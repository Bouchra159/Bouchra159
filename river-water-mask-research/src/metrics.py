"""
metrics.py
==========
Accuracy assessment metrics for water mask comparison.
Computes confusion matrix, F1, IoU, Kappa, Precision, Recall,
and supports bootstrapped confidence intervals and statistical tests.

Works with both numpy arrays (offline) and GEE-based confusion matrices.

References
----------
Fawcett (2006): ROC analysis
Foody (2002): Status of land cover classification accuracy assessment
"""

import numpy as np
from typing import Tuple, Dict, Optional
from scipy import stats


# ─────────────────────────────────────────────
# 1. Core Metrics (numpy-based, offline)
# ─────────────────────────────────────────────

def confusion_matrix_binary(y_true: np.ndarray,
                             y_pred: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Compute binary confusion matrix components.

    Parameters
    ----------
    y_true : np.ndarray
        Reference labels (1=water, 0=non-water).
    y_pred : np.ndarray
        Predicted labels (1=water, 0=non-water).

    Returns
    -------
    tuple
        (TP, FP, FN, TN)
    """
    y_true = np.asarray(y_true, dtype=int).flatten()
    y_pred = np.asarray(y_pred, dtype=int).flatten()

    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    return tp, fp, fn, tn


def compute_metrics(y_true: np.ndarray,
                    y_pred: np.ndarray) -> Dict[str, float]:
    """
    Compute all accuracy metrics for a binary water mask.

    Parameters
    ----------
    y_true : np.ndarray
        Reference labels (1=water, 0=non-water).
    y_pred : np.ndarray
        Predicted labels.

    Returns
    -------
    dict
        Dictionary with keys: precision, recall, f1, iou, kappa, oa,
        commission_error, omission_error, tp, fp, fn, tn.
    """
    tp, fp, fn, tn = confusion_matrix_binary(y_true, y_pred)
    n = tp + fp + fn + tn

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) > 0 else 0.0)
    iou = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0
    oa = (tp + tn) / n if n > 0 else 0.0

    # Cohen's Kappa
    po = oa
    pe = (((tp + fp) * (tp + fn) + (tn + fn) * (tn + fp)) / n**2) if n > 0 else 0.0
    kappa = (po - pe) / (1 - pe) if (1 - pe) > 0 else 0.0

    commission_error = fp / (tp + fp) if (tp + fp) > 0 else 0.0
    omission_error = fn / (tp + fn) if (tp + fn) > 0 else 0.0

    return {
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1': round(f1, 4),
        'iou': round(iou, 4),
        'kappa': round(kappa, 4),
        'overall_accuracy': round(oa, 4),
        'commission_error': round(commission_error, 4),
        'omission_error': round(omission_error, 4),
        'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
        'n_total': n,
    }


# ─────────────────────────────────────────────
# 2. Bootstrapped Confidence Intervals
# ─────────────────────────────────────────────

def bootstrap_metrics(y_true: np.ndarray, y_pred: np.ndarray,
                       metric: str = 'f1',
                       n_bootstrap: int = 1000,
                       ci: float = 0.95,
                       seed: int = 42) -> Dict[str, float]:
    """
    Compute bootstrapped confidence intervals for an accuracy metric.

    Parameters
    ----------
    y_true : np.ndarray
        Reference labels.
    y_pred : np.ndarray
        Predicted labels.
    metric : str
        Metric key from compute_metrics(). Default: 'f1'.
    n_bootstrap : int
        Number of bootstrap iterations. Default: 1000.
    ci : float
        Confidence level (0–1). Default: 0.95.
    seed : int
        Random seed for reproducibility. Default: 42.

    Returns
    -------
    dict
        {'mean': float, 'lower': float, 'upper': float, 'std': float}
    """
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()
    n = len(y_true)

    scores = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        m = compute_metrics(y_true[idx], y_pred[idx])
        scores.append(m[metric])

    scores = np.array(scores)
    alpha = 1 - ci
    lower = np.percentile(scores, 100 * alpha / 2)
    upper = np.percentile(scores, 100 * (1 - alpha / 2))

    return {
        'mean': round(float(np.mean(scores)), 4),
        'lower': round(float(lower), 4),
        'upper': round(float(upper), 4),
        'std': round(float(np.std(scores)), 4),
    }


# ─────────────────────────────────────────────
# 3. Statistical Tests
# ─────────────────────────────────────────────

def wilcoxon_test(scores_method_a: list, scores_method_b: list,
                  alpha: float = 0.05) -> Dict[str, float]:
    """
    Wilcoxon signed-rank test for paired method comparison.

    Use to determine if two methods have statistically different
    performance across multiple river/scene samples.

    Parameters
    ----------
    scores_method_a : list
        Metric scores (e.g., F1) for method A across scenes.
    scores_method_b : list
        Metric scores for method B across scenes.
    alpha : float
        Significance level. Default: 0.05.

    Returns
    -------
    dict
        {'statistic': float, 'p_value': float, 'significant': bool,
         'direction': str}
    """
    stat, p_value = stats.wilcoxon(scores_method_a, scores_method_b)
    significant = p_value < alpha
    mean_diff = np.mean(scores_method_a) - np.mean(scores_method_b)
    direction = 'A > B' if mean_diff > 0 else 'B > A' if mean_diff < 0 else 'equal'

    return {
        'statistic': round(float(stat), 4),
        'p_value': round(float(p_value), 6),
        'significant': significant,
        'direction': direction,
        'mean_a': round(float(np.mean(scores_method_a)), 4),
        'mean_b': round(float(np.mean(scores_method_b)), 4),
    }


# ─────────────────────────────────────────────
# 4. Temporal Consistency Index
# ─────────────────────────────────────────────

def temporal_consistency_index(water_area_series: np.ndarray) -> Dict[str, float]:
    """
    Compute temporal consistency index (TCI) for a water mask time series.

    TCI = 1 - (CV) where CV = std/mean (coefficient of variation).
    Higher TCI = more temporally stable mask.

    Parameters
    ----------
    water_area_series : np.ndarray
        Array of water area values (in km² or pixels) over time.

    Returns
    -------
    dict
        {'tci': float, 'cv': float, 'mean_area': float, 'std_area': float}
    """
    series = np.asarray(water_area_series, dtype=float)
    mean_area = float(np.mean(series))
    std_area = float(np.std(series))
    cv = std_area / mean_area if mean_area > 0 else 0.0
    tci = max(0.0, 1.0 - cv)

    return {
        'tci': round(tci, 4),
        'cv': round(cv, 4),
        'mean_area': round(mean_area, 2),
        'std_area': round(std_area, 2),
    }


# ─────────────────────────────────────────────
# 5. Comparison Report
# ─────────────────────────────────────────────

def compare_methods(results: Dict[str, Dict]) -> None:
    """
    Print a formatted comparison table of metrics across methods.

    Parameters
    ----------
    results : dict
        Dictionary mapping method names to their metrics dicts.
        Example: {'NDWI': compute_metrics(y_true, y_ndwi), ...}
    """
    metrics_to_show = ['precision', 'recall', 'f1', 'iou', 'kappa', 'overall_accuracy']
    header = f"{'Method':<20} " + " ".join(f"{m:>12}" for m in metrics_to_show)
    print(header)
    print("-" * len(header))
    for method, m in results.items():
        row = f"{method:<20} " + " ".join(f"{m.get(k, 0.0):>12.4f}" for k in metrics_to_show)
        print(row)
