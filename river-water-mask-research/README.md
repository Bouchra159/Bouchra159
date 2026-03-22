# River Water Mask Detection from Satellite Imagery
### SAR vs. Optical Methods: A Comparative Study

**Researcher:** Bouchra Daddaoui
**Supervisors:** Dr. Michael Nones (Institute of Geophysics, Polish Academy of Sciences) · Dr. Kaveh Ghahraman
**Affiliation:** Institute of Geophysics, Polish Academy of Sciences, Warsaw, Poland
**Contact:** bouchra1daddaoui@gmail.com
**Status:** Active Research (2025–2026)

---

## Project Overview

This research project investigates the comparative performance of **Synthetic Aperture Radar (SAR)** and **optical remote sensing** methods for extracting river water masks from large rivers at global scale. The study focuses on rivers selected from the **GLORIN (Global River Network)** dataset, spanning multiple latitudes and altitudes, to evaluate method robustness under diverse geophysical and atmospheric conditions.

### Research Questions

1. How accurately do optical-derived water masks (NDWI/MNDWI) capture river extent compared to SAR-derived masks across varying climatic and physiographic conditions?
2. Under what conditions (cloud cover, flood events, season, topography) does each method outperform the other?
3. What is the optimal integration strategy for combining SAR and optical data for consistent river mask generation?

---

## Working Plan

```
PHASE 1 — Literature Review (Weeks 1–4)
│
├── 1.1 Optical water index methods (NDWI, MNDWI, AWEI)
├── 1.2 SAR backscatter thresholding and classification
├── 1.3 Deep learning approaches for both modalities
├── 1.4 Existing global river mask datasets (JRC, HydroSAT, etc.)
└── 1.5 Summary matrix and gap analysis

PHASE 2 — River Selection & Data Acquisition (Weeks 3–6)
│
├── 2.1 Select 6–10 rivers from GLORIN (varying latitude & altitude)
├── 2.2 Download Sentinel-1 SAR data (GEE / Copernicus Hub)
├── 2.3 Download Sentinel-2 / Landsat-8/9 optical data (GEE)
└── 2.4 Preprocessing (geometric correction, radiometric calibration)

PHASE 3 — Water Mask Generation (Weeks 5–10)
│
├── 3.1 Optical: Compute NDWI, MNDWI, AWEI — threshold optimization
├── 3.2 SAR: Otsu thresholding, Lee filtering, change detection
├── 3.3 Deep learning baseline (optional): U-Net on Sentinel data
└── 3.4 Temporal stack analysis (dry / wet season comparison)

PHASE 4 — Comparative Analysis (Weeks 9–14)
│
├── 4.1 Accuracy assessment (IoU, F1, Kappa, OA)
├── 4.2 Cross-method consistency analysis
├── 4.3 Impact of cloud cover, season, river width on performance
└── 4.4 Statistical testing across river classes

PHASE 5 — Reporting (Weeks 13–18)
│
├── 5.1 Technical report (internal)
├── 5.2 Manuscript preparation (journal target: TBD)
└── 5.3 Presentation materials
```

---

## Repository Structure

```
.
├── README.md                       # This file
├── requirements.txt                # Python environment
├── environment.yml                 # Conda environment
│
├── docs/
│   ├── project_plan/
│   │   └── research_plan.md        # Detailed research plan
│   └── literature_review/
│       ├── optical_methods.md      # Optical remote sensing methods
│       ├── sar_methods.md          # SAR methods
│       ├── comparison_summary.md   # Cross-method comparison table
│       └── references.bib          # BibTeX references
│
├── data/
│   ├── README.md                   # Data sources and access instructions
│   └── river_selection/
│       ├── glorin_rivers.csv       # GLORIN candidate rivers
│       └── selected_rivers.md      # Final selection rationale
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # GEE data acquisition
│   ├── preprocessing.py            # SAR/optical preprocessing
│   ├── optical_masks.py            # NDWI, MNDWI, AWEI computation
│   ├── sar_masks.py                # SAR backscatter thresholding
│   ├── metrics.py                  # Accuracy metrics (IoU, F1, Kappa)
│   └── visualization.py            # Plotting and mapping utilities
│
├── notebooks/
│   ├── 01_data_exploration.ipynb   # EDA: imagery & river characteristics
│   ├── 02_optical_water_mask.ipynb # Optical mask generation pipeline
│   ├── 03_sar_water_mask.ipynb     # SAR mask generation pipeline
│   ├── 04_comparison_analysis.ipynb# Cross-method accuracy comparison
│   └── 05_reporting_figures.ipynb  # Final figures for publication
│
├── results/
│   ├── figures/                    # Output maps and plots
│   └── tables/                     # Accuracy assessment tables
│
└── reports/
    ├── internal_report_v1.md       # Internal progress report
    └── manuscript/                 # Journal manuscript (in progress)
```

---

## Selected Study Rivers (GLORIN-based)

| # | River | Country/Region | Latitude Zone | Altitude | Why Selected |
|---|-------|---------------|---------------|----------|--------------|
| 1 | Amazon | Brazil | Equatorial | Low | Largest discharge; persistent cloud cover challenge |
| 2 | Congo | DRC | Equatorial | Low-Mid | Dense cloud cover; tropical benchmark |
| 3 | Nile | Egypt/Sudan | Subtropical | Low-High | Arid conditions; optical advantage expected |
| 4 | Ganges | India/Bangladesh | Tropical | Low-High | Monsoon dynamics; high seasonal variability |
| 5 | Yangtze | China | Temperate | Low-High | Large altitudinal gradient; frequent floods |
| 6 | Mississippi | USA | Temperate | Low | Well-documented; validation data available |
| 7 | Rhine | Germany/Netherlands | Temperate | Low-Mid | Dense data availability; European benchmark |
| 8 | Ob | Russia | Subarctic | Low | Ice-affected; SAR advantage expected |

---

## Methods Summary

### Optical Methods
| Index | Formula | Optimal For |
|-------|---------|-------------|
| NDWI | (Green - NIR) / (Green + NIR) | Open water |
| MNDWI | (Green - SWIR) / (Green + SWIR) | Turbid water, built-up areas |
| AWEInsh | 4(Green - SWIR1) - (0.25·NIR + 2.75·SWIR2) | Non-shadow areas |
| AWEIsh | Blue + 2.5·Green - 1.5·(NIR + SWIR1) - 0.25·SWIR2 | Removing shadows |

### SAR Methods
| Method | Data | Approach |
|--------|------|----------|
| Otsu Thresholding | Sentinel-1 VV/VH | Global/local binary classification |
| Lee-Sigma Filter + Threshold | Sentinel-1 | Speckle-reduced backscatter |
| Bi-temporal Change Detection | Multi-date S1 | Flood mapping via change |
| Random Forest (SAR features) | S1 VV+VH+ratio | ML-based classification |

---

## Data Sources

| Dataset | Sensor | Resolution | Access | Use |
|---------|--------|-----------|--------|-----|
| Sentinel-1 GRD | C-band SAR | 10 m | Copernicus / GEE | SAR masks |
| Sentinel-2 L2A | Multispectral | 10 m | Copernicus / GEE | Optical masks |
| Landsat 8/9 | Multispectral | 30 m | USGS / GEE | Optical backup |
| JRC Global Surface Water | Optical composite | 30 m | GEE | Reference/validation |
| GLORIN | Vector | — | PANGAEA/Zenodo | River selection |
| HydroSHEDS | DEM | 90 m | HydroSHEDS.org | Basin delineation |
| SRTM / ALOS DEM | DEM | 30/12.5 m | USGS / JAXA | Elevation context |

---

## Research Standards

This project follows the standards of leading geoscience and remote sensing research institutions:

- **Reproducibility**: All analysis in version-controlled Jupyter notebooks; data access via GEE scripts
- **Open Science**: Code and results published openly; manuscript submitted to open-access or high-impact journal
- **Statistical Rigor**: Accuracy metrics computed with bootstrapped confidence intervals; cross-validated on held-out sites
- **FAIR Data Principles**: Findable, Accessible, Interoperable, Reusable data management
- **Documentation**: Every function documented with docstrings; methods section reproducible from code

---

## Getting Started

```bash
# Clone repository
git clone https://github.com/Bouchra159/Bouchra159.git
cd Bouchra159

# Create environment
conda env create -f environment.yml
conda activate river-masks

# Or with pip
pip install -r requirements.txt

# Launch notebooks
jupyter lab
```

---

## Contact & Collaboration

| Person | Role | Email |
|--------|------|-------|
| Bouchra Daddaoui | PhD Research Assistant | bouchra1daddaoui@gmail.com |
| Dr. Michael Nones | Principal Supervisor | mnones@igf.edu.pl |
| Dr. Kaveh Ghahraman | Co-Supervisor | — |

**Institution:** Institute of Geophysics, Polish Academy of Sciences
Ksiecia Janusza 64, 01-452 Warsaw, Poland

---

*Research conducted in collaboration with the Hydrology and Hydrodynamics Department, Institute of Geophysics PAS.*
