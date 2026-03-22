# Optical Remote Sensing Methods for River Water Mask Extraction

## Overview

Optical satellite imagery has been the backbone of large-scale surface water mapping for decades. This document reviews spectral index-based, threshold-based, and machine learning approaches applied to multispectral data for extracting river water masks.

---

## 1. Spectral Water Indices

### 1.1 Normalized Difference Water Index (NDWI)
**McFeeters (1996)**

$$NDWI = \frac{Green - NIR}{Green + NIR}$$

- **Bands used:** Green (~0.56 µm), Near-Infrared (NIR, ~0.86 µm)
- **Threshold:** Typically > 0 for water
- **Strength:** Effective for open, clear water bodies
- **Weakness:** Confused by built-up areas; poor performance in turbid rivers
- **Applicable sensors:** Sentinel-2 (B3/B8), Landsat-8 (B3/B5)

### 1.2 Modified NDWI (MNDWI)
**Xu (2006)**

$$MNDWI = \frac{Green - SWIR1}{Green + SWIR1}$$

- **Bands used:** Green (~0.56 µm), Short-Wave Infrared (SWIR1, ~1.6 µm)
- **Threshold:** Typically > 0 for water
- **Strength:** Suppresses built-up and vegetation signal; better for turbid/shallow water
- **Weakness:** Sensitive to wetland and flooded vegetation
- **Applicable sensors:** Sentinel-2 (B3/B11), Landsat-8 (B3/B6)

### 1.3 Automated Water Extraction Index (AWEI)
**Feyisa et al. (2014)**

Two variants:

**AWEInsh** (Non-Shadow):
$$AWEInsh = 4(Green - SWIR1) - (0.25 \cdot NIR + 2.75 \cdot SWIR2)$$

**AWEIsh** (Shadow):
$$AWEIsh = Blue + 2.5 \cdot Green - 1.5(NIR + SWIR1) - 0.25 \cdot SWIR2$$

- **Strength:** Explicitly handles shadow confusion and built-up surfaces
- **Weakness:** More complex; requires additional band calibration
- **Applicable sensors:** Landsat-8 (B2/B3/B5/B6/B7), Sentinel-2 (B2/B3/B8/B11/B12)

### 1.4 Water Ratio Index (WRI)
**Shen & Li (2010)**

$$WRI = \frac{Green + Red}{NIR + SWIR}$$

- **Threshold:** > 1 for water
- **Strength:** Simple ratio; good for bright water surfaces
- **Weakness:** Sensitive to sun glint and atmospheric effects

### 1.5 Normalized Difference Vegetation Index (NDVI) — inverse use

$$NDVI = \frac{NIR - Red}{NIR + Red}$$

- Water pixels typically have NDVI < 0
- Often combined with NDWI to exclude flooded vegetation

---

## 2. Thresholding Approaches

### 2.1 Global Fixed Threshold
- Most commonly used: threshold = 0 for NDWI/MNDWI
- Simple, reproducible, but not optimal across diverse regions

### 2.2 Otsu's Method (adaptive)
- Histogram-based bimodal optimization
- Globally minimizes intra-class variance between water/non-water
- **Best practice:** Apply at tile or watershed level, not globally
- Reference: Otsu (1979)

### 2.3 Multi-threshold / Mixture Models
- Gaussian Mixture Models (GMM) for ambiguous pixels
- Handles transition zones (e.g., flooded vegetation, wet soil)

---

## 3. Machine Learning Approaches

| Method | Input Features | Notes |
|--------|---------------|-------|
| Random Forest | Multi-band spectral + indices | High accuracy; requires training data |
| SVM | Spectral signatures | Good for small samples |
| U-Net (CNN) | RGB/multispectral tiles | State-of-the-art for dense segmentation |
| DeepWaterMap | Landsat multispectral | Pre-trained global model (Isikdogan et al., 2019) |

### Key Deep Learning References
- **Isikdogan et al. (2019)**: Surface water mapping by deep learning — DeepWaterMap trained on JRC Global Surface Water
- **Wieland & Martinis (2019)**: Large-scale flood mapping using SAR and optical DL fusion
- **Liangpei Zhang et al. (2022)**: Transformer-based models for multi-temporal water mapping

---

## 4. Benchmark Datasets for Validation

| Dataset | Year | Resolution | Source | Notes |
|---------|------|-----------|--------|-------|
| JRC Global Surface Water | 1984–present | 30 m | Pekel et al. (2016), Nature | Gold standard; Landsat-based |
| Global Inland Water (GIW) | 2000s | 250 m | MODIS | Coarser; good for large rivers |
| HydroLAKES | — | Vector | Messager et al. (2016) | Lake polygons |
| RivWidth / RiverObs | — | Sub-pixel | Pavelsky & Smith (2008) | Width measurements |
| SWOT satellite | 2023–present | ~100 m | NASA/CNES | New: water surface elevation + extent |

---

## 5. Key Challenges for Optical River Mapping

| Challenge | Impact | Mitigation |
|-----------|--------|-----------|
| Cloud cover | Missing data (especially tropical rivers) | Time-compositing; SAR fusion |
| Turbid water | Low NDWI signal | MNDWI preferred; NIR-Red combinations |
| Narrow rivers | Sub-pixel mixing | Higher resolution (S2 10m); spectral unmixing |
| Flooded vegetation | Index ambiguity | Combined NDWI+NDVI masking |
| Seasonal variation | Dynamic river extent | Multi-temporal stacking |
| Shadow | False positives | AWEIsh; DEM-based shadow modeling |
| Atmospheric interference | Signal distortion | Surface reflectance products (L2A) |

---

## 6. Key Papers to Review (Priority Reading List)

1. **McFeeters (1996)** — NDWI original paper. *Remote Sensing of Environment*, 57(2), 176–182.
2. **Xu (2006)** — MNDWI. *International Journal of Remote Sensing*, 27(14), 3025–3033.
3. **Feyisa et al. (2014)** — AWEI. *Remote Sensing of Environment*, 140, 23–35.
4. **Pekel et al. (2016)** — JRC Global Surface Water. *Nature*, 540, 418–422.
5. **Isikdogan et al. (2019)** — DeepWaterMap. *IEEE GRSL*, 17(6), 922–926.
6. **Yang et al. (2020)** — Mapping floods using optical and SAR imagery. *Remote Sensing*, 12, 2182.
7. **Jiang et al. (2021)** — Optical water mask comparison across rivers. *Remote Sensing of Environment*, 263, 112550.

---

## 7. Summary Assessment

| Method | Accuracy | Cloud Robustness | Computational Cost | Best For |
|--------|----------|-----------------|-------------------|---------|
| NDWI | Moderate | Low | Very Low | Clear, open water |
| MNDWI | Moderate–High | Low | Very Low | Turbid rivers |
| AWEI | High | Low | Low | Complex landscapes |
| Random Forest | High | Low | Medium | Supervised mapping |
| U-Net / DL | Very High | Low | High | Large-scale, automation |

> **Key insight:** Optical methods offer high spectral fidelity under clear conditions but systematically underperform in persistently cloudy regions (Amazon, Congo). SAR integration is essential for temporal completeness.
