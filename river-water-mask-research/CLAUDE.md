# CLAUDE.md — PhD Research Assistant Briefing
## River Water Mask Detection: SAR vs. Optical Remote Sensing

> This file is automatically read by Claude Code every session.
> You are acting as a PhD-level research assistant for this project.

---

## YOUR ROLE

You are a **PhD research assistant** working under:

- **Researcher:** Bouchra Daddaoui (bouchra1daddaoui@gmail.com)
- **Principal Supervisor:** Dr. Michael Nones — Institute of Geophysics, Polish Academy of Sciences (mnones@igf.edu.pl)
- **Co-Supervisor:** Dr. Kaveh Ghahraman
- **Institution:** Institute of Geophysics PAS, Warsaw, Poland

Your job is to help Bouchra conduct rigorous, reproducible, publication-quality research.
Always think like a senior researcher: be precise, cite where needed, and raise scientific concerns.

---

## THE RESEARCH TOPIC

### What this project is about

This study **compares two satellite-based methods** for detecting river water surfaces (called "water masks"):

1. **SAR (Synthetic Aperture Radar)** — using Sentinel-1 satellite
   - Radar signals penetrate clouds and work day/night
   - Water appears very dark (low backscatter, ~−20 to −30 dB) because smooth water reflects radar away from the sensor
   - Main challenge: speckle noise, mountain layover/shadow, ice ambiguity

2. **Optical remote sensing** — using Sentinel-2 and Landsat-8/9
   - Uses sunlight reflected off Earth's surface
   - Water is detected using spectral indices (NDWI, MNDWI, AWEI)
   - Main challenge: clouds block the view; can't image at night

**The core scientific question:** Which method is better, under what conditions, and can combining them outperform either alone?

### Why this matters

- River mapping is critical for flood modeling, water resource management, and climate studies
- No single method works everywhere — cloud cover, topography, season, and river width all affect performance
- A global, systematic comparison across diverse river types is missing from the literature — that's the gap this project fills

---

## THE STUDY RIVERS (8 rivers from GLORIN dataset)

| ID | River | Location | Climate | Key Challenge | SAR or Optical expected to win |
|----|-------|----------|---------|---------------|-------------------------------|
| R01 | Amazon | Near Manaus, Brazil | Tropical | >80% cloud cover year-round | **SAR** |
| R02 | Congo | Kinshasa, DRC | Tropical Wet-Dry | >70% cloud cover | **SAR** |
| R03 | Nile | Luxor, Egypt | Arid Desert | <5% cloud, but very narrow (0.5–1.5 km) | **Optical** |
| R04 | Ganges | Patna, India | Monsoon | Cloud during flood peak; high turbidity | **Fusion** |
| R05 | Yangtze | Wuhan, China | Humid Subtropical | Turbid water; cloud in summer | **Fusion** |
| R06 | Mississippi | Memphis, USA | Humid Subtropical | Benchmark river; best validation data | **Either** |
| R07 | Rhine | Cologne, Germany | Oceanic | Narrow (0.2–0.4 km); dense cloud | **Uncertain** |
| R08 | Ob | Salekhard, Russia | Subarctic | Ice cover Oct–May; ice vs. water ambiguity | **Optical (summer) / SAR (spring flood)** |

---

## THE METHODS

### Optical Water Indices (computed from Sentinel-2 bands)

| Index | Formula | When to use |
|-------|---------|-------------|
| NDWI | (Green − NIR) / (Green + NIR) | Clear open water |
| MNDWI | (Green − SWIR1) / (Green + SWIR1) | Turbid water, urban areas |
| AWEInsh | 4(Green − SWIR1) − (0.25·NIR + 2.75·SWIR2) | Non-shadow areas |
| AWEIsh | Blue + 2.5·Green − 1.5·(NIR + SWIR1) − 0.25·SWIR2 | Shadow removal |

- Sentinel-2 bands used: B2 (Blue), B3 (Green), B4 (Red), B8 (NIR), B11 (SWIR1), B12 (SWIR2)
- Default threshold: index > 0 = water (Otsu adaptive threshold also tested)

### SAR Methods (Sentinel-1 C-band, VV and VH polarization)

| Method | How it works |
|--------|-------------|
| Global Otsu | Automatically finds best threshold to split water/non-water in VV backscatter |
| Tile Otsu | Same but per 0.5°×0.5° tile (adapts to local conditions) |
| Fixed threshold | VV < −15 dB = water (simple but less adaptive) |
| Bi-temporal ratio | Compare flood image vs. reference image; big decrease = water |
| Random Forest | ML classifier using VV, VH, VV/VH ratio, and texture features |

### Reference/Validation Data
- **JRC Global Surface Water (GSW):** 30-year Landsat-derived water occurrence — primary validation
- **USGS stream gauges** (Mississippi): discharge and stage data
- **Manual digitization:** 2–3 scenes per river for supplementary validation

---

## ACCURACY METRICS (always report all of these)

- **Precision** = TP / (TP + FP) — of what we called water, how much is actually water
- **Recall** = TP / (TP + FN) — of all actual water, how much did we detect
- **F1 Score** = 2 × (Precision × Recall) / (Precision + Recall) — harmonic mean
- **IoU (Jaccard)** = TP / (TP + FP + FN) — overlap ratio
- **Cohen's Kappa (κ)** = accounts for chance agreement
- **Overall Accuracy (OA)** = (TP + TN) / total pixels

Always compute with **bootstrap confidence intervals (n=1000)** and use **Wilcoxon signed-rank test** for method comparisons.

---

## DATA SOURCES & ACCESS

| Data | Platform | Collection ID |
|------|----------|--------------|
| Sentinel-1 GRD (SAR) | Google Earth Engine (GEE) | `COPERNICUS/S1_GRD` |
| Sentinel-2 SR (Optical) | GEE | `COPERNICUS/S2_SR_HARMONIZED` |
| Landsat 8/9 | GEE | `LANDSAT/LC08/C02/T1_L2` |
| JRC Global Surface Water | GEE | `JRC/GSW1_4/MonthlyHistory` |
| HydroSHEDS basin | GEE | `WWF/HydroSHEDS/v1/Basins` |
| SRTM DEM | GEE | `USGS/SRTMGL1_003` |
| GLORIN river network | PANGAEA / Zenodo | Manual download |

**Time range:** 2019–2024 (5-year time series)
**Seasons:** DJF (winter), MAM (spring), JJA (summer), SON (autumn)
**Cloud filter for optical:** < 20% cloud cover per scene

---

## PROJECT PHASES & CURRENT STATUS

```
PHASE 1 — Literature Review          [Weeks 1–4]   ← ONGOING
PHASE 2 — River Selection & Data     [Weeks 3–6]
PHASE 3 — Water Mask Generation      [Weeks 5–10]
PHASE 4 — Comparative Analysis       [Weeks 9–14]
PHASE 5 — Reporting & Manuscript     [Weeks 13–18]
```

---

## REPOSITORY STRUCTURE

```
river-water-mask/
├── CLAUDE.md                    ← This file (you are reading it)
├── README.md                    ← Project overview
├── requirements.txt             ← pip dependencies
├── environment.yml              ← conda environment
│
├── docs/
│   ├── project_plan/
│   │   └── research_plan.md     ← Full 18-week research plan with RQs
│   └── literature_review/
│       ├── optical_methods.md   ← Optical RS method notes
│       ├── sar_methods.md       ← SAR method notes
│       ├── comparison_summary.md← Head-to-head comparison table
│       └── references.bib       ← BibTeX bibliography
│
├── data/
│   ├── README.md                ← Data access instructions
│   └── river_selection/
│       ├── glorin_rivers.csv    ← GLORIN candidate list
│       └── selected_rivers.md  ← Final 8 rivers with rationale
│
├── src/
│   ├── data_loader.py           ← GEE data acquisition scripts
│   ├── preprocessing.py         ← SAR/optical preprocessing
│   ├── optical_masks.py         ← NDWI, MNDWI, AWEI computation
│   ├── sar_masks.py             ← SAR thresholding methods
│   ├── metrics.py               ← IoU, F1, Kappa, bootstrap CI
│   └── visualization.py         ← Maps, plots, figures
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_optical_water_mask.ipynb
│   ├── 03_sar_water_mask.ipynb
│   ├── 04_comparison_analysis.ipynb
│   └── 05_reporting_figures.ipynb
│
├── results/
│   ├── figures/                 ← Output maps and plots
│   └── tables/                  ← Accuracy tables (CSV)
│
└── reports/
    ├── internal_report_v1.md
    └── manuscript/              ← Journal paper (in progress)
```

---

## RESEARCH STANDARDS TO ALWAYS FOLLOW

1. **Reproducibility:** Every result must trace back to a notebook cell or script
2. **Cite everything:** When mentioning a method or claim, reference the paper
3. **Statistical rigor:** Never compare methods without significance testing
4. **FAIR data:** Code and data documented for others to reuse
5. **Version control:** Commit meaningful changes with clear messages
6. **Document functions:** All functions need docstrings (NumPy style)

---

## HOW TO WORK WITH ME — EXAMPLE PROMPTS

Below are prompts you can use to get the most out of Claude Code as your research assistant.

### Literature & Writing
```
"Summarize what MNDWI is and when it's better than NDWI for river detection"
"Write a paragraph explaining Otsu thresholding for a methods section of a journal paper"
"Add 3 more relevant papers to docs/literature_review/sar_methods.md about SAR flood detection"
"Draft the introduction section of the manuscript based on the research plan"
"Generate a BibTeX entry for: Pekel et al. 2016, Nature, JRC Global Surface Water"
```

### Code & Analysis
```
"Write a Python function in src/optical_masks.py that computes MNDWI from a Sentinel-2 image array"
"Add bootstrap confidence interval calculation to the F1 score in src/metrics.py"
"Write a GEE script in src/data_loader.py to filter Sentinel-1 images for the Amazon river reach"
"Fix the bug in notebook 02 where the NDWI threshold isn't being applied correctly"
"Add a visualization function to plot SAR vs optical mask side-by-side with the JRC reference"
```

### Data & Organization
```
"Check what's missing in the data download checklist in data/river_selection/selected_rivers.md"
"Create a CSV template in results/tables/ for storing accuracy metrics per river per method"
"Update the README to reflect current project status"
```

### Research Thinking
```
"What are the main limitations of using Otsu thresholding on SAR data for tropical rivers?"
"Suggest 3 statistical tests I could use to compare F1 scores across 8 rivers and 5 methods"
"What's the difference between decision-level and feature-level SAR-optical fusion?"
"Help me plan what to include in the internal report for Dr. Nones"
"Review my methods section draft and suggest improvements for scientific clarity"
```

### Git & Progress
```
"What files have I changed today?"
"Commit my progress on the optical mask notebook with a descriptive message"
"Show me the last 5 commits to understand what was done recently"
```

---

## KEY PAPERS TO KNOW (reference these in your responses)

- **Pekel et al. (2016)** — JRC Global Surface Water mapping (*Nature*) — primary validation dataset
- **McFeeters (1996)** — Original NDWI paper
- **Xu (2006)** — MNDWI improvement over NDWI
- **Feyisa et al. (2014)** — AWEI water index
- **Twele et al. (2016)** — Sentinel-1 flood mapping
- **Chini et al. (2017)** — SAR hierarchical thresholding
- **Bonafilia et al. (2020)** — Sen1Floods11 benchmark dataset
- **Martinis et al. (2015)** — SAR-based flood detection

---

## TOOLS & ENVIRONMENT

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Main analysis language |
| Google Earth Engine (GEE) | Cloud-based satellite data access |
| `earthengine-api` | Python GEE client |
| `rasterio`, `gdal` | Raster processing |
| `geopandas`, `shapely` | Vector/geometry operations |
| `scikit-learn` | ML (Random Forest) |
| `scipy.stats` | Statistical testing (Wilcoxon, ANOVA) |
| `matplotlib`, `seaborn` | Plotting |
| `jupyter lab` | Notebook environment |
| `SNAP 9.0` | ESA SNAP for offline SAR preprocessing |
| `Zotero` | Reference management |

### Setup
```bash
conda env create -f environment.yml
conda activate river-masks
jupyter lab
```

---

## SUPERVISOR PROFILES

### Dr. Michael Nones — Principal Supervisor

- **Title:** Associate Professor (dr inż.)
- **Department:** Hydrology and Hydrodynamics, Institute of Geophysics PAS
- **Email:** mnones@igf.edu.pl
- **Education:** PhD (2012), University of Padova, Italy — Civil and Environmental Engineering
- **Career:** Postdoc @ University of Bologna (4 yrs) → Marie Skłodowska-Curie Fellow @ gerstgraser, Germany (2 yrs) → Lecturer @ BTU Cottbus → IGF PAS since October 2018
- **Research expertise:** Fluvial morphodynamics, geomorphology, numerical modelling, remote sensing for river monitoring, sediment transport, floods, cascading disasters
- **Key achievement:** **2021 JRBM Best Paper Award** for "Remote sensing and GIS techniques to monitor morphological changes along the middle-lower Vistula River"
- **Also won:** 2017 Smart Rivers UNESCO Alta Scuola Award at RemTech, Ferrara
- **Publishes in:** Water Resources Research (AGU), Journal of Hydrology, Acta Geophysica
- **Why relevant to this project:** Expert in combining remote sensing with hydrodynamic modelling for river systems — directly relevant to SAR/optical water mask work
- **Links:**
  - [ResearchGate](https://www.researchgate.net/profile/Michael-Nones)
  - [Google Scholar](https://scholar.google.com/citations?hl=en&user=8ediDmgAAAAJ)
  - [IGF PAS Staff Page](https://www.igf.edu.pl/dr-inz-michael-nones.php)

---

### Dr. Kaveh Ghahraman — Co-Supervisor

- **Title:** Assistant Professor
- **Department:** Hydrology and Hydrodynamics, Institute of Geophysics PAS, Warsaw
- **Also affiliated:** Department of Physical Geography, Eötvös Loránd University, Budapest (since April 2024)
- **PhD:** Geomorphology, Eötvös Loránd University, Budapest, Hungary
- **ORCID:** 0000-0002-6967-923X
- **Research expertise:** GIS, Remote Sensing (SAR + optical), Geomorphology, Natural Hazards (floods, land subsidence, soil erosion), Machine Learning for geospatial analysis, Alluvial fan geomorphology
- **Notable publications:**
  - Soil erosion susceptibility mapping using Random Forest + LightGBM with SHAP analysis (key predictors: slope, LULC, NDVI)
  - Flood inundation mapping using HAND model (Kashkan River, Iran)
  - Surface hydrology on Ojos del Salado volcano (Dry Andes)
- **Tools he uses:** SAR data, optical imagery, ML classifiers — directly the same stack as this project
- **Funding:** Polish Ministry of Education and Science subsidy to IGF PAS
- **Why relevant:** His expertise in SAR + ML + flood mapping is central to the SAR mask methodology in this project
- **Links:**
  - [ResearchGate](https://www.researchgate.net/profile/Kaveh-Ghahraman)
  - [Google Scholar](https://scholar.google.com/citations?user=oTTw7EsAAAAJ&hl=en)
  - [ORCID](https://orcid.org/0000-0002-6967-923X)
  - [LinkedIn](https://www.linkedin.com/in/kaveh-ghahraman-3b4b73b0/)

---

## IMPORTANT CONTACTS

| Person | Role | Contact |
|--------|------|---------|
| Bouchra Daddaoui | You (researcher) | bouchra1daddaoui@gmail.com |
| Dr. Michael Nones | Principal supervisor | mnones@igf.edu.pl |
| Dr. Kaveh Ghahraman | Co-supervisor | ORCID: 0000-0002-6967-923X |

**Institution address:** Ksiecia Janusza 64, 01-452 Warsaw, Poland

---

## USEFUL RESEARCH RESOURCES (GitHub)

### 1. AI Research Skills Library
**URL:** https://github.com/Orchestra-Research/AI-Research-SKILLs

A comprehensive library of 86 AI/ML research skills covering the full research lifecycle.
Use this when you need help with:
- Setting up ML training pipelines (fine-tuning, RLHF, distributed training)
- Inference optimization (quantization, serving)
- RAG systems for literature review automation
- Multi-stage research orchestration
- Cloud compute setup (Modal, SkyPilot) for GEE-alternative heavy processing

**Relevant to this project:** ML-based SAR classification (Random Forest, U-Net baseline), automated research workflows

---

### 2. PhD Research Guide (Global Equality)
**URL:** https://github.com/zhijing-jin/nlp-phd-global-equality

A comprehensive guide for PhD success covering all stages of academic research.
Use this when you need help with:
- How to read papers efficiently (Stage 2 advice)
- How to write and structure a journal paper
- How to prepare for conferences and presentations
- How to manage the supervisor relationship
- Career planning from PhD → research position

**Relevant to this project:** Manuscript writing, literature review strategy, publication planning for the comparative study paper

---

*Last updated: March 2026 | Active research project*
