# Internal Progress Report — v1
## River Water Mask Study: SAR vs. Optical Remote Sensing

**Date:** March 2025
**Researcher:** Bouchra Daddaoui
**To:** Dr. Michael Nones, Dr. Kaveh Ghahraman
**Status:** Phase 1 — Repository Setup & Literature Review in Progress

---

## Executive Summary

This report documents the initial setup of the research project on comparative river water mask extraction using SAR and optical satellite imagery. The research infrastructure has been established, the literature review framework is underway, and the study river selection from the GLORIN dataset has been completed.

---

## 1. Completed Tasks

### 1.1 Repository & Infrastructure
- [x] GitHub repository initialized with structured layout
- [x] Research directory structure created
- [x] Python environment specification (requirements.txt, environment.yml)
- [x] Source modules developed: data_loader, optical_masks, sar_masks, metrics, visualization
- [x] Jupyter notebook templates for full analysis pipeline
- [x] `.gitignore` configured for geospatial research

### 1.2 River Selection (GLORIN-based)
- [x] 14 candidate rivers screened from GLORIN
- [x] **8 rivers selected** covering:
  - 5 climate zones (tropical, arid, monsoon, temperate, subarctic)
  - Latitudes from 3°S to 66°N
  - Altitudes from 10 m (Ob) to 280 m (Congo)
- [x] Data availability assessment methodology prepared

### 1.3 Literature Review (In Progress)
- [x] Optical methods framework documented (NDWI, MNDWI, AWEI, DL)
- [x] SAR methods framework documented (Otsu, tile-based, change detection, DL)
- [x] Cross-method comparison table created
- [x] Priority reading list established (20+ key papers identified)
- [x] BibTeX reference file created (25 key references)

---

## 2. Selected Rivers Summary

| River | Country | Climate | Key Challenge |
|-------|---------|---------|--------------|
| Amazon | Brazil | Tropical Rainforest | >80% cloud cover |
| Congo | DRC | Tropical Wet-Dry | >70% cloud cover |
| Nile | Egypt | Arid Desert | Narrow width, regulated |
| Ganges | India | Tropical Monsoon | Monsoon cloud cover |
| Yangtze | China | Humid Subtropical | Turbidity |
| Mississippi | USA | Humid Subtropical | Benchmark river |
| Rhine | Germany | Oceanic | Narrow width |
| Ob | Russia | Subarctic | Ice cover |

---

## 3. Methodology Summary

### Optical Methods (5 variants)
- NDWI, MNDWI, AWEInsh, AWEIsh (fixed and Otsu thresholds)

### SAR Methods (5 variants)
- Fixed threshold (VV < -15 dB)
- Global Otsu (VV)
- Tile-based adaptive Otsu (0.5° tiles)
- Bi-temporal change detection (log-ratio)
- Random Forest (VV, VH, VV/VH features)

### Reference: JRC Global Surface Water
- Monthly history product (1984–present, 30 m resolution)
- Resampled to 10 m for S1/S2 comparison

### Accuracy Assessment
- Metrics: Precision, Recall, F1, IoU, Cohen's Kappa, OA
- Bootstrapped 95% confidence intervals (n=1000)
- Wilcoxon signed-rank test for pairwise comparison

---

## 4. Next Steps (Phase 2)

**Priority for next 2 weeks:**
1. Complete literature review reading (optical + SAR methods papers)
2. Authenticate GEE account and run data availability assessment
3. Download/export initial test data for one river (Mississippi — best validation data)
4. Run preliminary optical masks and verify against JRC reference
5. Set up meeting to discuss preliminary results

---

## 5. Open Questions for Supervisors

1. **Journal target**: Which journal do you recommend for submission? (e.g., Remote Sensing of Environment, Remote Sensing, JHM, HESS?)
2. **GLORIN access**: Can you share the specific GLORIN dataset file/DOI to ensure correct river reach coordinates?
3. **Validation priority**: Should we prioritize accuracy metrics, or also include river width analysis?
4. **Fusion approach**: Should the fusion experiment be included in the initial paper or treated as future work?

---

## 6. Timeline Status

```
✅ Week 1–2:  Repository + literature framework
⏳ Week 3–4:  Complete literature review reading
⏳ Week 4–5:  GEE data acquisition setup
⏳ Week 5–7:  Preprocessing pipeline
⏳ Week 7–9:  Optical masks
⏳ Week 8–10: SAR masks
⏳ Week 10–12: Accuracy assessment
⏳ Week 12–13: Statistical analysis
⏳ Week 13–14: Fusion experiments
⏳ Week 14–18: Reporting & manuscript
```

---

*Next meeting suggested: Upon completion of Phase 2 (data acquisition)*
*Contact: bouchra1daddaoui@gmail.com*
