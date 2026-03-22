# SAR vs. Optical: Comparative Summary for River Water Mask Extraction

## Head-to-Head Comparison Matrix

| Criterion | Optical (Sentinel-2 / Landsat) | SAR (Sentinel-1) |
|-----------|-------------------------------|------------------|
| **Spatial resolution** | 10 m (S2), 30 m (L8) | 10 m (S1 IW GRD) |
| **Temporal resolution** | 5 days (S2), 16 days (L8) | 6 days (S1) |
| **Cloud penetration** | No | Yes |
| **Night imaging** | No | Yes |
| **Water spectral contrast** | Very High (NDWI up to 1.0 for clear water) | High (−20 to −30 dB) |
| **Turbid water detection** | Moderate (MNDWI better) | Good |
| **Narrow river detection** | Better (strong spectral contrast) | Weaker (speckle, layover) |
| **Flooded vegetation** | Poor (spectral confusion) | Good (double-bounce, L-band) |
| **Mountain rivers** | Moderate | Poor (layover/shadow) |
| **Tropical rivers** | Poor (cloud cover) | Excellent |
| **Arid rivers** | Excellent | Good |
| **Ice-affected rivers** | Difficult | Possible (if unfrozen) |
| **Data cost** | Free (S2, L8) | Free (S1) |
| **Processing complexity** | Low–Medium | Medium–High |
| **Automation maturity** | High | High |
| **Deep learning readiness** | Very High | High |

---

## Performance by Climate Zone

| Climate Zone | Expected Best Method | Reasoning |
|-------------|---------------------|-----------|
| Tropical (Amazon, Congo) | **SAR** | Persistent cloud cover defeats optical |
| Monsoon (Ganges, Yangtze) | **SAR + Optical fusion** | SAR for cloud periods; Optical for dry season |
| Arid/Semiarid (Nile) | **Optical** | Clear skies; high reflectance contrast |
| Temperate (Mississippi, Rhine) | **Either / Fusion** | Variable cloud cover; both adequate |
| Subarctic (Ob) | **Optical (summer) / SAR (winter)** | Ice affects both; seasonal strategy needed |
| Alpine/Mountain | **Optical** | SAR layover problematic in steep terrain |

---

## Performance by River Characteristic

| River Property | Optical Performance | SAR Performance |
|---------------|--------------------|-----------------|
| Width > 100 m | Excellent | Excellent |
| Width 30–100 m | Good | Moderate |
| Width < 30 m | Poor (subpixel) | Poor (subpixel + speckle) |
| High discharge (flood) | Moderate | Excellent |
| Low flow (dry season) | Good | Good |
| Turbid water | Moderate (MNDWI) | Good |
| Clear water | Excellent (NDWI) | Good |
| Braided channel | Moderate | Moderate |
| Anastomosing | Good | Moderate |
| Floodplain inundation | Moderate | Excellent |

---

## Accuracy Reported in Literature

| Study | Region | Optical (OA %) | SAR (OA %) | Notes |
|-------|--------|---------------|-----------|-------|
| Twele et al. (2016) | Global floods | ~88% | ~92% | Flood events |
| Jiang et al. (2021) | China rivers | 94% (MNDWI) | 89% (Otsu) | Cloud-free periods |
| Schlaffer et al. (2015) | Danube | — | 91% (change det.) | Flood |
| Yang et al. (2020) | Multi-region | 91% | 88% | Average clear sky |
| Bonafilia et al. (2020) | 11 flood events | — | 84% (RF) | Benchmark |
| DeepWaterMap (2019) | Global | 96% | — | JRC validation |

> Note: Direct comparisons are rare; most studies focus on one modality. A key contribution of this project is systematic side-by-side evaluation.

---

## Fusion Strategies

When neither method alone is sufficient, fusion approaches combine their strengths:

### 1. Decision-Level Fusion
- Generate binary masks independently from SAR and optical
- Combine via logical OR (maximize recall) or AND (maximize precision)
- **Strength:** Simple, modular
- **Weakness:** Does not use synergistic information

### 2. Feature-Level Fusion
- Stack SAR and optical bands as input to ML classifier
- Random Forest or CNN trained on combined features
- **Strength:** Leverages both data types
- **Weakness:** Requires co-registration; cloud mask needed for optical

### 3. Score/Probability Fusion
- Produce soft probability maps from each modality
- Weight and combine (e.g., cloud-weighted: give SAR full weight under clouds)
- **Strength:** Handles missing data gracefully
- **Best practice for this study**

### 4. Temporal Compositing
- Optical: cloud-free composite over time window
- SAR: temporal median to reduce speckle and wind effects
- Combined for permanent water mask
- Reference: Pekel et al. (2016) approach

---

## Recommended Reading Order for This Project

### Week 1: Foundations
- [ ] Pekel et al. (2016) — JRC Global Surface Water (*Nature*)
- [ ] Huang et al. (2018) — Review: detecting surface water (*Earth-Science Reviews*)

### Week 2: Optical methods
- [ ] McFeeters (1996) — NDWI
- [ ] Xu (2006) — MNDWI
- [ ] Feyisa et al. (2014) — AWEI
- [ ] Isikdogan et al. (2019) — DeepWaterMap

### Week 3: SAR methods
- [ ] Martinis et al. (2015) — SAR flood detection
- [ ] Twele et al. (2016) — Sentinel-1 water mapping
- [ ] Chini et al. (2017) — SAR thresholding hierarchy
- [ ] Bonafilia et al. (2020) — Sen1Floods11

### Week 4: Comparative and fusion studies
- [ ] Yang et al. (2020) — Optical + SAR fusion
- [ ] Bates et al. (2021) — Fluvial remote sensing review
- [ ] Jiang et al. (2021) — Optical river mask comparison
- [ ] Sentinel-1/2 fusion papers (search: "SAR optical fusion water mapping")

---

## Research Gaps (Opportunities for This Study)

1. **Systematic multi-river evaluation** at global scale covering diverse climates and altitudes — most studies are region-specific
2. **GLORIN-aligned benchmarking** — few studies use GLORIN for river selection
3. **Altitude gradient analysis** — impact of terrain on both SAR (layover) and optical (shadow, snow) not well characterized
4. **Seasonal consistency analysis** — which method gives more temporally stable masks?
5. **River width thresholds** — at what river width does each method become unreliable?
