# Data Directory

## Structure

```
data/
├── README.md                    # This file
├── river_selection/
│   ├── glorin_rivers.csv        # Candidate rivers from GLORIN (14 candidates)
│   └── selected_rivers.md       # Final 8 rivers with rationale and profiles
├── raw/                         # Downloaded satellite data (NOT committed to git — too large)
│   ├── sentinel1/               # SAR GRD products per river
│   ├── sentinel2/               # S2 L2A products per river
│   └── jrc_gsw/                 # JRC Global Surface Water reference
└── processed/                   # Processed masks and intermediate products
    ├── optical_masks/
    ├── sar_masks/
    └── accuracy_tables/
```

## Data Sources

### Satellite Data (Primary)

| Dataset | Source | Access | Format | Notes |
|---------|--------|--------|--------|-------|
| Sentinel-1 GRD | Copernicus | GEE / ASF | GeoTIFF | VV+VH, IW mode |
| Sentinel-2 L2A | Copernicus | GEE / SciHub | GeoTIFF | 10m bands |
| Landsat 8/9 | USGS | GEE | GeoTIFF | 30m backup |

### Reference Data (Validation)

| Dataset | Source | Resolution | Notes |
|---------|--------|-----------|-------|
| JRC Global Surface Water | GEE: `JRC/GSW1_4/MonthlyHistory` | 30 m | Primary reference |
| HydroSHEDS | `WWF/HydroSHEDS/v1` | 90 m | Basin boundaries |
| SRTM DEM | `USGS/SRTMGL1_003` | 30 m | Elevation context |

## Data Access via GEE

See `src/data_loader.py` for GEE data loading scripts.

Quick start:
```python
from src.data_loader import RiverDataLoader

loader = RiverDataLoader(river_id='R01', start_date='2020-01-01', end_date='2020-12-31')
s1_collection = loader.get_sentinel1()
s2_collection = loader.get_sentinel2(max_cloud=20)
jrc_reference = loader.get_jrc_reference()
```

## Important Notes

- Raw satellite data is **NOT stored in this repository** (too large for git)
- Use GEE for cloud-based processing; export to Google Drive if needed
- All processed outputs should be stored in `processed/` with clear naming conventions
- Naming convention: `{river_id}_{sensor}_{method}_{date}.tif`
  - Example: `R01_S1_OtsuVV_20200601.tif`

## GLORIN Dataset

The **GLORIN (Global River Information)** dataset provides a standardized set of large river reaches globally. For access and citation, refer to the official GLORIN publication and data repository.

Key attributes used for river selection:
- Mean annual discharge (m³/s)
- River width statistics
- Geographic coordinates of representative reaches
- River order and basin area
