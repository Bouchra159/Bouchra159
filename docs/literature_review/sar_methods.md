# SAR-Based Methods for River Water Mask Extraction

## Overview

Synthetic Aperture Radar (SAR) is an all-weather, day-night active microwave sensor that has become indispensable for surface water monitoring. This document reviews the physical basis, algorithmic methods, and current state of the art for SAR-based river mask extraction.

---

## 1. Physical Basis of SAR Water Detection

### 1.1 Backscatter Principles
- **Smooth water surfaces** act as specular reflectors → very **low backscatter** (typically -20 to -30 dB for VV/VH)
- **Rough water / flood water with vegetation** can appear brighter due to double-bounce
- **C-band SAR** (5.6 cm wavelength, Sentinel-1) is the standard for water mapping
- **L-band SAR** (23 cm, ALOS-2/PALSAR) penetrates vegetation — better for flooded forests

### 1.2 Polarimetric Channels
| Channel | Physical Meaning | Water Sensitivity |
|---------|-----------------|------------------|
| VV (Vertical–Vertical) | Surface scattering dominant | High — best for open water |
| VH (Vertical–Horizontal) | Volume/cross scattering | Moderate — lower for smooth water |
| VV/VH ratio | Backscatter ratio | Good water discriminator |
| HH (Horizontal–Horizontal) | L-band, double-bounce | Flooded vegetation |

### 1.3 Key Sentinel-1 Specifications
- **Wavelength:** 5.6 cm (C-band)
- **Modes:** IW (Interferometric Wide Swath) — primary for land mapping
- **Resolution:** 10 m (IW GRD product)
- **Polarization:** VV+VH (land), HH+HV (sea ice)
- **Revisit time:** ~6 days (global), ~3 days (European)
- **Data access:** Free via Copernicus Open Access Hub / Google Earth Engine

---

## 2. Preprocessing Pipeline

```
Raw GRD Product
    │
    ├── Apply Orbit File
    │
    ├── Thermal Noise Removal
    │
    ├── Radiometric Calibration → Sigma0 (dB)
    │
    ├── Speckle Filtering
    │   ├── Lee Filter (7x7 window)
    │   ├── Lee-Sigma Filter
    │   ├── Gamma-MAP Filter
    │   └── Refined Lee Filter (recommended)
    │
    ├── Range Doppler Terrain Correction (SRTM DEM)
    │
    └── Conversion to dB (10 * log10(sigma0))
```

**Software:** ESA SNAP (open source), Google Earth Engine (cloud-based), ASF HyP3

---

## 3. Thresholding Methods

### 3.1 Global Fixed Threshold
- Water is typically below -15 dB (VV) or -20 dB (VH)
- Simple but not generalizable across regions and seasons

### 3.2 Otsu's Bimodal Threshold
- Most widely used for SAR water mapping
- Assumes bimodal histogram (water vs. land)
- **Limitation:** Fails if one class dominates image area
- **Best practice:** Apply at local tile level (e.g., 1° × 1° tiles)

### 3.3 Tile-Based Adaptive Threshold (Martinis et al., 2015)
- Subdivide scene into tiles; apply Otsu per tile
- Aggregated via Gaussian weighting
- Handles spatial non-stationarity of backscatter

### 3.4 KI (Kittler-Illingworth) Threshold
- Minimum description length approach
- More robust than Otsu under uneven class distributions
- Reference: Kittler & Illingworth (1986)

### 3.5 Region Growing
- Seed pixels (certain water) → grow region based on connectivity and backscatter
- Reduces salt-and-pepper noise
- Combined with flood fill algorithms

---

## 4. Advanced SAR Methods

### 4.1 Multi-temporal Analysis
- Change detection: Δbackscatter between dry and flood image
- Ratio image: σ_flood / σ_reference
- Log-ratio: 10 log(σ_flood / σ_reference) — normalized change
- **Very effective for flood mapping**; removes permanent water confusion

### 4.2 Polarimetric Decomposition
- For fully polarimetric data (PolSAR): Freeman-Durden, Pauli decomposition
- Separates surface, volume, double-bounce scattering mechanisms
- Flooded forests show strong double-bounce signature

### 4.3 Coherence-Based Methods
- InSAR coherence drops over water (temporal decorrelation)
- Low coherence + low backscatter → strong water indicator
- Requires interferometric pair (same track, short baseline)

### 4.4 Machine Learning on SAR Features
| Features Used | Method | Reference |
|--------------|--------|-----------|
| VV, VH, VV/VH ratio | Random Forest | Many studies |
| Texture (GLCM) | SVM | Twele et al. (2016) |
| Time-series statistics | LSTM | Rußwurm et al. (2020) |
| Sentinel-1 tiles | U-Net (CNN) | Bonafilia et al. (2020) |

### 4.5 Deep Learning for SAR Water Mapping
- **SpaceNet-6:** SAR-based building segmentation (transferable architectures)
- **Sen1Floods11 (Bonafilia et al., 2020):** Benchmark dataset for flood mapping with Sentinel-1
  - 11 flood events; 4,831 labeled chips; available on GitHub
  - Baseline models: Random Forest, Semi-supervised CNN
- **FDSI (Flood Detection and Segmentation Index):** Deep ensemble for multi-source fusion

---

## 5. River-Specific SAR Challenges

| Challenge | Description | Mitigation |
|-----------|------------|-----------|
| Wind-roughened water | Higher backscatter → missed water | Multi-look filtering; wind data masking |
| Emergent vegetation | Double-bounce false positive | NDVI masking from optical |
| Layover/shadow (mountains) | Geometric distortion in incidence angle | DEM-based simulation mask |
| Narrow rivers | Width < 1–2 resolution cells | Subpixel SAR; fusion with optical |
| Braided channels | Complex geometry | High-resolution SAR (Sentinel-1 EW? TerraSAR-X) |
| Ice cover | High backscatter from ice | Seasonal mask; freeze/thaw index |
| Rain events | C-band signal attenuation | L-band preferred; flag rainy scenes |
| Smooth non-water surfaces | Roads, parking lots | Context filters; elevation |

---

## 6. Operational SAR-Based Water Products

| Product | Method | Resolution | Temporal | Source |
|---------|--------|-----------|----------|--------|
| Copernicus EMS | Manual + Otsu | 10–30 m | Event-based | ESA |
| GFM (Global Flood Monitor) | Bayesian SAR | 20 m | Near real-time | TU Wien |
| VIIRS-based NOAA | SAR + IR fusion | 375 m | Daily | NOAA |
| DRFN / JRC SAR | Sentinel-1 | 10 m | Monthly | JRC (developing) |
| HydroSAT | Sentinel-1 + DEM | 10 m | Time-series | DLR |

---

## 7. Key Papers to Review (Priority Reading List)

1. **Martinis et al. (2015)** — Towards operational near real-time flood detection using SAR. *Remote Sensing*, 7(7), 8197–8214.
2. **Twele et al. (2016)** — Sentinel-1 flood mapping. *Remote Sensing Letters*, 7(8), 768–777.
3. **Bonafilia et al. (2020)** — Sen1Floods11. *CVPR Workshops*.
4. **Bates et al. (2021)** — Combined use of SAR and optical for fluvial remote sensing. *Annual Review of Earth and Planetary Sciences*, 49.
5. **Schlaffer et al. (2015)** — Flood detection from multi-temporal SAR data. *ISPRS JPRS*, 104, 203–219.
6. **Chini et al. (2017)** — Hierarchical split-based approach for parametric thresholding. *IEEE TGRS*, 55(12), 6975–6988.
7. **Huang et al. (2018)** — Detecting, extracting, and monitoring surface water. *Earth-Science Reviews*, 169, 140–164.

---

## 8. Summary Assessment

| Method | All-Weather | Flood Mapping | Vegetation Penetration | Cost | Maturity |
|--------|------------|--------------|----------------------|------|---------|
| Otsu Threshold | Yes | Good | None (C-band) | Low | High |
| Adaptive Tile-Otsu | Yes | Very Good | None | Low | High |
| Change Detection | Yes | Excellent | None | Low | High |
| PolSAR Decomposition | Yes | Good | Partial (L-band) | Medium | Medium |
| U-Net on SAR | Yes | Excellent | Depends on training | High | Emerging |
| SAR + InSAR coherence | Yes | Good | Some | Medium | Medium |

> **Key insight:** SAR provides all-weather capability critical for cloud-prone river systems (Amazon, Congo, Ganges during monsoon). However, it struggles with narrow rivers and wind-roughened surfaces where optical indices perform well.
