"""
data_loader.py
==============
Google Earth Engine data acquisition for river water mask study.
Provides functions to load Sentinel-1 (SAR), Sentinel-2 (optical),
and reference datasets (JRC GSW) for selected river reaches.

Usage:
    import ee
    ee.Initialize()

    from src.data_loader import RiverDataLoader
    loader = RiverDataLoader('R01', '2020-01-01', '2020-12-31')
    s1 = loader.get_sentinel1()
    s2 = loader.get_sentinel2()
    jrc = loader.get_jrc_reference()
"""

import ee
import pandas as pd
from pathlib import Path

# River geometry definitions (center + buffer)
RIVER_CONFIG = {
    'R01': {'name': 'Amazon',      'lat': -3.1,  'lon': -60.0, 'buffer_km': 30},
    'R02': {'name': 'Congo',       'lat': -4.3,  'lon':  15.3, 'buffer_km': 25},
    'R03': {'name': 'Nile',        'lat': 25.7,  'lon':  32.6, 'buffer_km': 10},
    'R04': {'name': 'Ganges',      'lat': 25.6,  'lon':  85.1, 'buffer_km': 20},
    'R05': {'name': 'Yangtze',     'lat': 30.6,  'lon': 114.3, 'buffer_km': 20},
    'R06': {'name': 'Mississippi', 'lat': 35.1,  'lon': -90.0, 'buffer_km': 20},
    'R07': {'name': 'Rhine',       'lat': 50.9,  'lon':   6.9, 'buffer_km': 10},
    'R08': {'name': 'Ob',          'lat': 66.5,  'lon':  66.6, 'buffer_km': 25},
}


class RiverDataLoader:
    """Load and prepare satellite data for a given river reach."""

    def __init__(self, river_id: str, start_date: str, end_date: str):
        """
        Parameters
        ----------
        river_id : str
            River identifier (e.g., 'R01' for Amazon).
        start_date : str
            Start date in 'YYYY-MM-DD' format.
        end_date : str
            End date in 'YYYY-MM-DD' format.
        """
        if river_id not in RIVER_CONFIG:
            raise ValueError(f"Unknown river_id '{river_id}'. Choose from: {list(RIVER_CONFIG.keys())}")

        self.river_id = river_id
        self.config = RIVER_CONFIG[river_id]
        self.start_date = start_date
        self.end_date = end_date

        # Define area of interest
        center = ee.Geometry.Point([self.config['lon'], self.config['lat']])
        self.aoi = center.buffer(self.config['buffer_km'] * 1000)

    def get_sentinel1(self, orbit_pass: str = 'ASCENDING',
                      polarizations: list = None) -> ee.ImageCollection:
        """
        Load Sentinel-1 GRD collection for the river reach.

        Parameters
        ----------
        orbit_pass : str
            'ASCENDING' or 'DESCENDING'. Default: 'ASCENDING'.
        polarizations : list
            List of polarizations to select. Default: ['VV', 'VH'].

        Returns
        -------
        ee.ImageCollection
            Filtered and calibrated Sentinel-1 collection (sigma0 in dB).
        """
        if polarizations is None:
            polarizations = ['VV', 'VH']

        collection = (
            ee.ImageCollection('COPERNICUS/S1_GRD')
            .filterBounds(self.aoi)
            .filterDate(self.start_date, self.end_date)
            .filter(ee.Filter.eq('orbitProperties_pass', orbit_pass))
            .filter(ee.Filter.eq('instrumentMode', 'IW'))
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
            .select(polarizations)
        )
        return collection

    def get_sentinel2(self, max_cloud: int = 20,
                      apply_cloud_mask: bool = True) -> ee.ImageCollection:
        """
        Load Sentinel-2 Surface Reflectance collection.

        Parameters
        ----------
        max_cloud : int
            Maximum scene cloud cover percentage. Default: 20%.
        apply_cloud_mask : bool
            Apply SCL-based cloud/shadow mask. Default: True.

        Returns
        -------
        ee.ImageCollection
            Cloud-masked Sentinel-2 collection (reflectance, scaled 0–1).
        """
        collection = (
            ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(self.aoi)
            .filterDate(self.start_date, self.end_date)
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', max_cloud))
            .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'SCL'])
        )

        if apply_cloud_mask:
            collection = collection.map(_mask_s2_clouds)

        # Scale to [0, 1]
        collection = collection.map(lambda img: img.divide(10000).copyProperties(img, img.propertyNames()))
        return collection

    def get_jrc_reference(self) -> ee.ImageCollection:
        """
        Load JRC Global Surface Water monthly history as reference.

        Returns
        -------
        ee.ImageCollection
            JRC monthly water occurrence maps (0=no water, 2=water).
        """
        jrc = (
            ee.ImageCollection('JRC/GSW1_4/MonthlyHistory')
            .filterBounds(self.aoi)
            .filterDate(self.start_date, self.end_date)
        )
        return jrc

    def get_dem(self) -> ee.Image:
        """Load SRTM DEM clipped to AOI."""
        return ee.Image('USGS/SRTMGL1_003').clip(self.aoi)

    def get_aoi(self) -> ee.Geometry:
        """Return the area of interest geometry."""
        return self.aoi

    def get_info(self) -> dict:
        """Return river metadata."""
        return {
            'river_id': self.river_id,
            'name': self.config['name'],
            'center': (self.config['lat'], self.config['lon']),
            'buffer_km': self.config['buffer_km'],
            'date_range': (self.start_date, self.end_date),
        }


def _mask_s2_clouds(image: ee.Image) -> ee.Image:
    """Apply Sentinel-2 Scene Classification Layer (SCL) cloud/shadow mask."""
    scl = image.select('SCL')
    # SCL values: 3=cloud shadow, 8=cloud medium prob, 9=cloud high prob, 10=thin cirrus
    cloud_shadow = scl.eq(3)
    cloud_medium = scl.eq(8)
    cloud_high = scl.eq(9)
    cirrus = scl.eq(10)
    mask = cloud_shadow.Or(cloud_medium).Or(cloud_high).Or(cirrus).Not()
    return image.updateMask(mask).select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])


def load_river_table(csv_path: str = None) -> pd.DataFrame:
    """
    Load the river selection table.

    Parameters
    ----------
    csv_path : str, optional
        Path to glorin_rivers.csv. Defaults to data/river_selection/glorin_rivers.csv.

    Returns
    -------
    pd.DataFrame
        River metadata table.
    """
    if csv_path is None:
        csv_path = Path(__file__).parents[1] / 'data' / 'river_selection' / 'glorin_rivers.csv'
    return pd.read_csv(csv_path)


def get_selected_rivers() -> pd.DataFrame:
    """Return only the selected (YES) rivers from the GLORIN candidate table."""
    df = load_river_table()
    return df[df['selected'] == 'YES'].reset_index(drop=True)
