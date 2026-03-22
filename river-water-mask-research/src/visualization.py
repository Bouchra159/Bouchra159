"""
visualization.py
================
Plotting and mapping utilities for the river water mask comparison study.
Provides publication-quality figures for accuracy comparison, water masks,
temporal analysis, and cross-method performance charts.

Uses matplotlib, seaborn, and rasterio for visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from pathlib import Path
from typing import Optional, Dict, List, Tuple


# ─────────────────────────────────────────────
# Global Plot Style (publication-ready)
# ─────────────────────────────────────────────

plt.rcParams.update({
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'legend.framealpha': 0.9,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Method color palette
METHOD_COLORS = {
    'NDWI':       '#2196F3',
    'MNDWI':      '#4CAF50',
    'MNDWI-Otsu': '#8BC34A',
    'AWEInsh':    '#FF9800',
    'AWEIsh':     '#FF5722',
    'SAR-Fixed':  '#9C27B0',
    'SAR-Otsu':   '#673AB7',
    'SAR-Tile':   '#3F51B5',
    'SAR-Change': '#00BCD4',
    'SAR-RF':     '#009688',
    'Fusion':     '#F44336',
}

RIVER_MARKERS = {
    'Amazon': 'o', 'Congo': 's', 'Nile': '^', 'Ganges': 'D',
    'Yangtze': 'v', 'Mississippi': 'P', 'Rhine': 'X', 'Ob': '*',
}


# ─────────────────────────────────────────────
# 1. Accuracy Comparison Plots
# ─────────────────────────────────────────────

def plot_accuracy_comparison(results: Dict[str, Dict],
                              metric: str = 'f1',
                              title: str = None,
                              save_path: Optional[str] = None) -> plt.Figure:
    """
    Bar chart comparing accuracy metrics across methods.

    Parameters
    ----------
    results : dict
        Method name → metrics dict (from metrics.compute_metrics).
    metric : str
        Metric to plot ('f1', 'iou', 'kappa', etc.).
    title : str, optional
        Plot title.
    save_path : str, optional
        Path to save figure. If None, figure is displayed.

    Returns
    -------
    plt.Figure
    """
    methods = list(results.keys())
    values = [results[m].get(metric, 0) for m in methods]
    colors = [METHOD_COLORS.get(m, '#607D8B') for m in methods]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(methods, values, color=colors, edgecolor='white', linewidth=1.2)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f'{val:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel('Method')
    ax.set_ylabel(metric.upper())
    ax.set_ylim(0, 1.05)
    ax.set_title(title or f'{metric.upper()} Score by Method')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig


def plot_metrics_heatmap(results_per_river: Dict[str, Dict[str, Dict]],
                          metric: str = 'f1',
                          save_path: Optional[str] = None) -> plt.Figure:
    """
    Heatmap of accuracy metric across methods × rivers.

    Parameters
    ----------
    results_per_river : dict
        {river_name: {method_name: metrics_dict}}
    metric : str
        Metric to display.
    save_path : str, optional
        Save path for figure.

    Returns
    -------
    plt.Figure
    """
    rivers = list(results_per_river.keys())
    methods = list(next(iter(results_per_river.values())).keys())

    matrix = np.array([
        [results_per_river[r][m].get(metric, 0) for m in methods]
        for r in rivers
    ])

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        matrix,
        annot=True, fmt='.3f',
        xticklabels=methods,
        yticklabels=rivers,
        cmap='YlOrRd',
        vmin=0, vmax=1,
        linewidths=0.5,
        ax=ax,
        cbar_kws={'label': metric.upper()}
    )
    ax.set_title(f'{metric.upper()} Score: Methods × Rivers', pad=15)
    ax.set_xlabel('Method')
    ax.set_ylabel('River')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig


# ─────────────────────────────────────────────
# 2. Temporal Analysis Plots
# ─────────────────────────────────────────────

def plot_water_area_timeseries(dates: List, area_optical: List,
                                area_sar: List,
                                river_name: str,
                                discharge: Optional[List] = None,
                                save_path: Optional[str] = None) -> plt.Figure:
    """
    Time series of water area from optical and SAR methods.

    Parameters
    ----------
    dates : list
        List of datetime objects.
    area_optical : list
        Water area (km²) from optical method.
    area_sar : list
        Water area (km²) from SAR method.
    river_name : str
        River name for title.
    discharge : list, optional
        Discharge data for secondary axis.
    save_path : str, optional
        Save path.

    Returns
    -------
    plt.Figure
    """
    fig, ax1 = plt.subplots(figsize=(14, 5))

    ax1.plot(dates, area_optical, '-o', color=METHOD_COLORS['MNDWI'],
             label='Optical (MNDWI)', markersize=4, linewidth=1.5)
    ax1.plot(dates, area_sar, '-s', color=METHOD_COLORS['SAR-Otsu'],
             label='SAR (Otsu)', markersize=4, linewidth=1.5)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Water Area (km²)')
    ax1.set_title(f'Water Extent Time Series — {river_name}')
    ax1.legend(loc='upper left')

    if discharge is not None:
        ax2 = ax1.twinx()
        ax2.fill_between(dates, discharge, alpha=0.15, color='#607D8B')
        ax2.plot(dates, discharge, '-', color='#607D8B', linewidth=1, label='Discharge (m³/s)')
        ax2.set_ylabel('Discharge (m³/s)', color='#607D8B')
        ax2.tick_params(axis='y', labelcolor='#607D8B')
        ax2.legend(loc='upper right')

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig


# ─────────────────────────────────────────────
# 3. Binary Mask Visualization
# ─────────────────────────────────────────────

def plot_mask_comparison(reference: np.ndarray,
                          optical_mask: np.ndarray,
                          sar_mask: np.ndarray,
                          river_name: str,
                          save_path: Optional[str] = None) -> plt.Figure:
    """
    Side-by-side comparison of reference, optical, and SAR water masks.

    Parameters
    ----------
    reference : np.ndarray
        Reference water mask (1=water, 0=land).
    optical_mask : np.ndarray
        Optical-derived water mask.
    sar_mask : np.ndarray
        SAR-derived water mask.
    river_name : str
        River name for titles.
    save_path : str, optional
        Save path.

    Returns
    -------
    plt.Figure
    """
    cmap_water = mcolors.ListedColormap(['#f5f5f5', '#1565C0'])

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    axes[0].imshow(reference, cmap=cmap_water, vmin=0, vmax=1)
    axes[0].set_title('Reference (JRC GSW)')

    axes[1].imshow(optical_mask, cmap=cmap_water, vmin=0, vmax=1)
    axes[1].set_title('Optical Mask (MNDWI)')

    axes[2].imshow(sar_mask, cmap=cmap_water, vmin=0, vmax=1)
    axes[2].set_title('SAR Mask (Otsu VV)')

    # Agreement map
    agreement = np.zeros_like(reference)
    agreement[(reference == 1) & (optical_mask == 1) & (sar_mask == 1)] = 4  # All agree: water
    agreement[(reference == 0) & (optical_mask == 0) & (sar_mask == 0)] = 3  # All agree: land
    agreement[(reference == 1) & (optical_mask == 1) & (sar_mask == 0)] = 2  # Optical only
    agreement[(reference == 1) & (optical_mask == 0) & (sar_mask == 1)] = 1  # SAR only

    cmap_agreement = mcolors.ListedColormap(['#BDBDBD', '#03A9F4', '#8BC34A', '#F5F5F5', '#1565C0'])
    axes[3].imshow(agreement, cmap=cmap_agreement, vmin=0, vmax=4)
    axes[3].set_title('Agreement Map')

    for ax in axes:
        ax.axis('off')

    fig.suptitle(f'Water Mask Comparison — {river_name}', fontsize=14, fontweight='bold')
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig


# ─────────────────────────────────────────────
# 4. Climate Zone Performance Summary
# ─────────────────────────────────────────────

def plot_climate_performance(river_metadata: Dict,
                              f1_optical: Dict[str, float],
                              f1_sar: Dict[str, float],
                              save_path: Optional[str] = None) -> plt.Figure:
    """
    Scatter plot: F1 optical vs. SAR per river, colored by climate zone.

    Parameters
    ----------
    river_metadata : dict
        {river_name: {'climate_zone': str, ...}}
    f1_optical : dict
        {river_name: f1_score}
    f1_sar : dict
        {river_name: f1_score}
    save_path : str, optional
        Save path.
    """
    climate_colors = {
        'Tropical Rainforest': '#E53935',
        'Tropical Wet-Dry': '#FB8C00',
        'Arid Desert': '#FDD835',
        'Tropical Monsoon': '#43A047',
        'Humid Subtropical': '#1E88E5',
        'Oceanic': '#8E24AA',
        'Subarctic': '#00ACC1',
    }

    fig, ax = plt.subplots(figsize=(8, 8))

    for river, meta in river_metadata.items():
        f1_opt = f1_optical.get(river, 0)
        f1_s = f1_sar.get(river, 0)
        climate = meta.get('climate_zone', 'Unknown')
        color = climate_colors.get(climate, '#607D8B')
        marker = RIVER_MARKERS.get(river, 'o')

        ax.scatter(f1_opt, f1_s, c=color, marker=marker, s=150,
                   edgecolors='black', linewidth=0.8, zorder=5, label=river)
        ax.annotate(river, (f1_opt, f1_s), textcoords='offset points',
                    xytext=(6, 4), fontsize=9)

    # Diagonal: equal performance line
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, label='Equal performance')
    ax.fill_between([0, 1], [0, 1], [1, 1], alpha=0.05, color='purple',
                    label='SAR better region')
    ax.fill_between([0, 1], [0, 0], [0, 1], alpha=0.05, color='blue',
                    label='Optical better region')

    ax.set_xlabel('F1 Score — Optical (MNDWI)')
    ax.set_ylabel('F1 Score — SAR (Otsu VV)')
    ax.set_title('Optical vs. SAR Performance by River\n(Above diagonal: SAR better)')
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower right', fontsize=8)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
    return fig
