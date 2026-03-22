# Detailed Research Plan
## River Water Mask Comparison: SAR vs. Optical Remote Sensing

**PI:** Dr. Michael Nones (mnones@igf.edu.pl)
**Co-PI:** Dr. Kaveh Ghahraman
**Research Assistant:** Bouchra Daddaoui
**Institution:** Institute of Geophysics, Polish Academy of Sciences
**Duration:** ~18 weeks (approx. April–August 2025)

---

## 1. Project Objectives

### Primary Objective
Systematically compare the performance of SAR-based (Sentinel-1) and optical-based (Sentinel-2/Landsat) water mask extraction methods across a globally representative set of large rivers.

### Secondary Objectives
- Identify the conditions (climate, season, river width, altitude) under which each method excels or fails
- Produce river-specific recommendations for operational water mask generation
- Build a reproducible, open-source analysis pipeline
- Contribute to the scientific literature with a peer-reviewed publication

---

## 2. Research Questions

| # | Research Question | Expected Outcome |
|---|------------------|-----------------|
| RQ1 | How do NDWI/MNDWI-based optical masks compare to Otsu SAR masks in terms of accuracy (F1, IoU, Kappa)? | Quantitative performance table per river |
| RQ2 | Does cloud cover percentage correlate with optical mask quality degradation? | Regression model: cloud cover vs. accuracy |
| RQ3 | How does river width affect detection accuracy for both methods? | Width-accuracy curves |
| RQ4 | What is the seasonal consistency of each method? | Temporal consistency index (TCI) |
| RQ5 | Which method better captures flood extent during peak discharge? | Flood event comparison |
| RQ6 | Can a fusion approach consistently outperform either single method? | Fusion vs. single method accuracy |

---

## 3. Study Area: River Selection

### Selection Criteria (GLORIN-based)
1. River is listed in GLORIN with mean annual discharge > 1,000 m³/s
2. At least one river per major climate zone (tropical, subtropical, temperate, subarctic)
3. Coverage of low, mid, and high altitude (< 200 m, 200–1000 m, > 1000 m a.s.l.)
4. Availability of validation data (JRC GSW, SWOT, or field measurements)
5. No major dam interference with natural flow regime (or documented impact)

### Final River Selection

| ID | River | Reach | Lat (°) | Lon (°) | Altitude (m) | Mean Q (m³/s) | Climate | Key Challenge |
|----|-------|-------|---------|---------|-------------|--------------|---------|--------------|
| R01 | Amazon | Near Manaus, BR | -3.1 | -60.0 | ~40 | ~120,000 | Tropical | Cloud cover |
| R02 | Congo | Kinshasa, DRC | -4.3 | 15.3 | ~280 | ~41,000 | Tropical | Cloud cover |
| R03 | Nile | Luxor reach, EG | 25.7 | 32.6 | ~80 | ~2,800 | Arid | Narrow width |
| R04 | Ganges | Patna reach, IN | 25.6 | 85.1 | ~55 | ~12,000 | Monsoon | Seasonal change |
| R05 | Yangtze | Wuhan reach, CN | 30.6 | 114.3 | ~23 | ~22,000 | Temperate | Turbidity |
| R06 | Mississippi | Memphis reach, US | 35.1 | -90.0 | ~75 | ~16,000 | Temperate | Benchmark |
| R07 | Rhine | Köln, DE | 50.9 | 6.9 | ~37 | ~2,300 | Temperate | Dense data |
| R08 | Ob | Salekhard, RU | 66.5 | 66.6 | ~10 | ~12,800 | Subarctic | Ice cover |

---

## 4. Data Acquisition Strategy

### Satellite Data
- **Platform:** Google Earth Engine (GEE) — primary
- **Backup:** Copernicus Open Access Hub (manual download)

#### Sentinel-1 (SAR)
```python
# GEE filter criteria
collection = 'COPERNICUS/S1_GRD'
orbit_pass = 'ASCENDING'  # and DESCENDING separately
instrument_mode = 'IW'
polarization = ['VV', 'VH']
date_range = ['2019-01-01', '2024-12-31']  # 5-year time series
```

#### Sentinel-2 (Optical)
```python
collection = 'COPERNICUS/S2_SR_HARMONIZED'  # Surface Reflectance
cloud_filter = 20  # < 20% cloud cover per scene
date_range = ['2019-01-01', '2024-12-31']
bands = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']  # Blue, Green, Red, NIR, SWIR1, SWIR2
```

#### Reference Data
- JRC Global Surface Water (GSW): `JRC/GSW1_4/MonthlyHistory`
- HydroSHEDS river mask: `WWF/HydroSHEDS/v1/Basins`
- SRTM DEM: `USGS/SRTMGL1_003`

### Temporal Strategy
- **Primary period:** 5 years (2019–2024) for temporal analysis
- **Seasonal samples:** 4 images per year per river (DJF, MAM, JJA, SON representative)
- **Flood events:** Minimum 2 documented flood events per river

---

## 5. Preprocessing Pipeline

### SAR Preprocessing (via GEE or SNAP)
```
GRD product → Apply orbit file → Thermal noise removal
           → Radiometric calibration (sigma0)
           → Refined Lee speckle filter (7×7)
           → Range Doppler terrain correction (SRTM)
           → Convert to dB
```

### Optical Preprocessing
```
S2 L2A (already surface reflectance)
       → Cloud masking (SCL band: QA60 or s2cloudless)
       → TOA → SR (already done for L2A)
       → Compute indices (NDWI, MNDWI, AWEI)
```

---

## 6. Water Mask Generation

### 6.1 Optical Masks

| Mask ID | Method | Formula | Threshold |
|---------|--------|---------|-----------|
| OPT-01 | NDWI | (B3-B8)/(B3+B8) | > 0 |
| OPT-02 | MNDWI | (B3-B11)/(B3+B11) | > 0 |
| OPT-03 | MNDWI-Otsu | MNDWI + Otsu | Adaptive |
| OPT-04 | AWEInsh | 4(B3-B11)-(0.25·B8+2.75·B12) | > 0 |
| OPT-05 | AWEIsh | B2+2.5·B3-1.5·(B8+B11)-0.25·B12 | > 0 |

### 6.2 SAR Masks

| Mask ID | Method | Input | Threshold |
|---------|--------|-------|-----------|
| SAR-01 | Global Otsu | VV (dB) | Otsu |
| SAR-02 | Tile Otsu | VV (dB), 0.5°×0.5° tiles | Adaptive Otsu |
| SAR-03 | Fixed threshold | VV (dB) | -15 dB |
| SAR-04 | Bi-temporal ratio | VV flood / VV reference | log-ratio > 3 dB |
| SAR-05 | Random Forest | VV, VH, VV/VH, texture | ML |

### 6.3 Reference Mask
- JRC GSW Monthly History (30 m) → resampled to 10 m via bilinear interpolation
- Manual digitization for 2–3 scenes per river as supplementary validation

---

## 7. Accuracy Assessment

### Metrics

$$Precision = \frac{TP}{TP + FP}$$

$$Recall = \frac{TP}{TP + FN}$$

$$F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$$

$$IoU = \frac{TP}{TP + FP + FN}$$

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where: TP = True Positive (correctly mapped water), FP = False Positive (non-water mapped as water), FN = False Negative (missed water), TN = True Negative (correctly mapped non-water)

### Sampling Strategy
- Stratified random sampling: 500 points per image (250 water, 250 non-water)
- Bootstrap confidence intervals (n=1000) for all metrics
- Significance testing: Wilcoxon signed-rank test for pairwise method comparison

---

## 8. Statistical Analysis

### Planned Analyses

1. **ANOVA** — test if accuracy differences across methods are statistically significant
2. **Multiple regression** — predictor variables: cloud cover %, river width, season, altitude, discharge → response: accuracy (F1)
3. **Cluster analysis** — group rivers by method performance pattern
4. **Temporal consistency index** — coefficient of variation of monthly mask area over 5 years

---

## 9. Deliverables & Timeline

| Week | Phase | Deliverable |
|------|-------|------------|
| 1–2 | Literature | Draft lit. review outline |
| 3–4 | Literature | Full literature review (optical + SAR methods) |
| 4–5 | Data | GLORIN river selection finalized; GEE scripts ready |
| 5–7 | Data | All satellite data downloaded/processed |
| 7–9 | Processing | Optical water masks for all rivers |
| 8–10 | Processing | SAR water masks for all rivers |
| 10–12 | Analysis | Accuracy assessment complete |
| 12–13 | Analysis | Statistical analysis complete |
| 13–14 | Analysis | Fusion experiment results |
| 14–15 | Reporting | Draft internal report |
| 15–16 | Reporting | Presentation materials |
| 16–18 | Reporting | Manuscript draft |

---

## 10. Meeting Schedule

- **Progress meetings:** Upon completion of each phase (not fixed schedule)
- **Check-in:** Email updates monthly or when a milestone is reached
- **Contacts:** Dr. Michael Nones (primary), Dr. Kaveh Ghahraman, Raveena (peer student)

---

## 11. Tools & Software

| Tool | Purpose | License |
|------|---------|---------|
| Google Earth Engine | Data access & cloud processing | Free (research) |
| Python 3.11+ | Analysis & visualization | Open source |
| SNAP 9.0 | SAR preprocessing (offline) | Free (ESA) |
| GDAL/Rasterio | Raster operations | Open source |
| GeoPandas | Vector operations | Open source |
| Scikit-learn | Machine learning | Open source |
| Matplotlib / Seaborn | Plotting | Open source |
| Jupyter Lab | Notebook environment | Open source |
| Git / GitHub | Version control | Free |
| Zotero | Reference management | Free |

---

## 12. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| GEE quota limits | Medium | Medium | Batch processing; export to Drive |
| Missing Sentinel-1 coverage | Low | Medium | Use available passes; note gaps |
| JRC GSW validation gaps | Medium | Medium | Manual digitization supplement |
| Cloud cover > 80% all seasons | Low (tropical) | High | SAR-only analysis for affected rivers |
| Paper rejection | Medium | Low | Pre-submission peer review; choose right journal |
