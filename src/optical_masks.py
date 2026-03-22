"""
optical_masks.py
================
Optical water index computation and threshold-based water mask generation.
Supports NDWI, MNDWI, AWEInsh, AWEIsh for Sentinel-2 imagery.

All functions operate on Google Earth Engine Image objects.

References
----------
McFeeters (1996): NDWI
Xu (2006): MNDWI
Feyisa et al. (2014): AWEI
Otsu (1979): Histogram-based adaptive threshold
"""

import ee
import numpy as np


# ─────────────────────────────────────────────
# 1. Spectral Water Index Computation
# ─────────────────────────────────────────────

def compute_ndwi(image: ee.Image) -> ee.Image:
    """
    Normalized Difference Water Index (McFeeters, 1996).

    NDWI = (Green - NIR) / (Green + NIR)
    Sentinel-2 bands: B3 (Green), B8 (NIR)

    Parameters
    ----------
    image : ee.Image
        Sentinel-2 image with bands B3 and B8 (scaled 0–1).

    Returns
    -------
    ee.Image
        NDWI image (range: -1 to 1). Band named 'NDWI'.
    """
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    return image.addBands(ndwi)


def compute_mndwi(image: ee.Image) -> ee.Image:
    """
    Modified NDWI (Xu, 2006).

    MNDWI = (Green - SWIR1) / (Green + SWIR1)
    Sentinel-2 bands: B3 (Green), B11 (SWIR1)

    Parameters
    ----------
    image : ee.Image
        Sentinel-2 image with bands B3 and B11 (scaled 0–1).

    Returns
    -------
    ee.Image
        Image with added MNDWI band (range: -1 to 1).
    """
    mndwi = image.normalizedDifference(['B3', 'B11']).rename('MNDWI')
    return image.addBands(mndwi)


def compute_awei_nsh(image: ee.Image) -> ee.Image:
    """
    Automated Water Extraction Index — Non-Shadow (Feyisa et al., 2014).

    AWEInsh = 4*(Green - SWIR1) - (0.25*NIR + 2.75*SWIR2)
    Sentinel-2: B3, B11, B8, B12

    Parameters
    ----------
    image : ee.Image
        Sentinel-2 image with bands B3, B8, B11, B12 (scaled 0–1).

    Returns
    -------
    ee.Image
        Image with added AWEInsh band.
    """
    green = image.select('B3')
    nir = image.select('B8')
    swir1 = image.select('B11')
    swir2 = image.select('B12')

    awei_nsh = (
        green.multiply(4).subtract(swir1.multiply(4))
        .subtract(nir.multiply(0.25).add(swir2.multiply(2.75)))
        .rename('AWEInsh')
    )
    return image.addBands(awei_nsh)


def compute_awei_sh(image: ee.Image) -> ee.Image:
    """
    Automated Water Extraction Index — Shadow (Feyisa et al., 2014).

    AWEIsh = Blue + 2.5*Green - 1.5*(NIR + SWIR1) - 0.25*SWIR2
    Sentinel-2: B2, B3, B8, B11, B12

    Parameters
    ----------
    image : ee.Image
        Sentinel-2 image with bands B2, B3, B8, B11, B12 (scaled 0–1).

    Returns
    -------
    ee.Image
        Image with added AWEIsh band.
    """
    blue = image.select('B2')
    green = image.select('B3')
    nir = image.select('B8')
    swir1 = image.select('B11')
    swir2 = image.select('B12')

    awei_sh = (
        blue
        .add(green.multiply(2.5))
        .subtract(nir.add(swir1).multiply(1.5))
        .subtract(swir2.multiply(0.25))
        .rename('AWEIsh')
    )
    return image.addBands(awei_sh)


def compute_all_indices(image: ee.Image) -> ee.Image:
    """Compute NDWI, MNDWI, AWEInsh, AWEIsh for a Sentinel-2 image."""
    image = compute_ndwi(image)
    image = compute_mndwi(image)
    image = compute_awei_nsh(image)
    image = compute_awei_sh(image)
    return image


# ─────────────────────────────────────────────
# 2. Threshold-Based Water Mask Generation
# ─────────────────────────────────────────────

def apply_fixed_threshold(image: ee.Image, band: str,
                           threshold: float = 0.0) -> ee.Image:
    """
    Apply a fixed threshold to generate a binary water mask.

    Parameters
    ----------
    image : ee.Image
        Image containing the target band.
    band : str
        Band name (e.g., 'NDWI', 'MNDWI').
    threshold : float
        Threshold value. Pixels >= threshold are water (1). Default: 0.

    Returns
    -------
    ee.Image
        Binary water mask (1=water, 0=non-water). Band named 'water_mask'.
    """
    water_mask = image.select(band).gte(threshold).rename('water_mask')
    return water_mask


def apply_otsu_threshold(image: ee.Image, band: str,
                          aoi: ee.Geometry, scale: int = 30) -> ee.Image:
    """
    Apply Otsu's method for adaptive threshold selection.

    Computes histogram of the band within the AOI and finds the
    threshold that minimizes intra-class variance (bimodal assumption).

    Parameters
    ----------
    image : ee.Image
        Image containing the target band.
    band : str
        Band name (e.g., 'MNDWI').
    aoi : ee.Geometry
        Area of interest for histogram computation.
    scale : int
        Spatial scale (m) for histogram sampling. Default: 30 m.

    Returns
    -------
    ee.Image
        Binary water mask (1=water, 0=non-water).
    """
    # Compute histogram
    histogram = image.select(band).reduceRegion(
        reducer=ee.Reducer.histogram(255, 0.001),
        geometry=aoi,
        scale=scale,
        maxPixels=1e10
    ).get(band)

    # Compute Otsu threshold via GEE function
    threshold = _otsu_gee(histogram)
    water_mask = image.select(band).gte(threshold).rename('water_mask')
    return water_mask


def _otsu_gee(histogram) -> ee.Number:
    """
    Server-side Otsu threshold computation in GEE.

    Implements within-class variance minimization using bucket counts.
    """
    counts = ee.Array(ee.Dictionary(histogram).get('histogram'))
    means = ee.Array(ee.Dictionary(histogram).get('bucketMeans'))
    size = means.length().get([0])
    total = counts.reduce(ee.Reducer.sum(), [0]).get([0])
    sum_ = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0])
    mean = sum_.divide(total)

    indices = ee.List.sequence(1, size)

    def compute_bsv(i):
        """Between-class variance for split at index i."""
        i = ee.Number(i).toInt()
        count_a = counts.slice(0, 0, i).reduce(ee.Reducer.sum(), [0]).get([0])
        count_b = counts.slice(0, i).reduce(ee.Reducer.sum(), [0]).get([0])
        mean_a = ee.Algorithms.If(
            count_a.gt(0),
            means.slice(0, 0, i).multiply(counts.slice(0, 0, i))
            .reduce(ee.Reducer.sum(), [0]).get([0]).divide(count_a),
            0
        )
        mean_b = ee.Algorithms.If(
            count_b.gt(0),
            means.slice(0, i).multiply(counts.slice(0, i))
            .reduce(ee.Reducer.sum(), [0]).get([0]).divide(count_b),
            0
        )
        weight_a = count_a.divide(total)
        weight_b = count_b.divide(total)
        bsv = weight_a.multiply(weight_b).multiply(
            ee.Number(mean_a).subtract(mean_b).pow(2)
        )
        return bsv

    bsvs = ee.Array(indices.map(compute_bsv))
    max_idx = bsvs.argmax().get([0])
    threshold = means.get([max_idx])
    return threshold


# ─────────────────────────────────────────────
# 3. Time-Series Water Mask (Compositing)
# ─────────────────────────────────────────────

def generate_seasonal_composite(collection: ee.ImageCollection,
                                 band: str = 'MNDWI',
                                 reducer: str = 'median') -> ee.Image:
    """
    Generate a seasonal composite image from a collection.

    Parameters
    ----------
    collection : ee.ImageCollection
        Sentinel-2 collection with computed water index bands.
    band : str
        Index band to composite. Default: 'MNDWI'.
    reducer : str
        Aggregation method: 'median', 'mean', 'max'. Default: 'median'.

    Returns
    -------
    ee.Image
        Composite image.
    """
    reducers = {
        'median': ee.Reducer.median(),
        'mean': ee.Reducer.mean(),
        'max': ee.Reducer.max(),
    }
    if reducer not in reducers:
        raise ValueError(f"reducer must be one of {list(reducers.keys())}")
    return collection.select(band).reduce(reducers[reducer]).rename(band)


def generate_monthly_water_frequency(collection: ee.ImageCollection,
                                      threshold: float = 0.0) -> ee.Image:
    """
    Compute monthly water occurrence frequency from a time-series.

    Each pixel value = fraction of months detected as water.

    Parameters
    ----------
    collection : ee.ImageCollection
        Collection of binary water masks (1=water, 0=non-water).
    threshold : float
        Index threshold for water classification. Default: 0.

    Returns
    -------
    ee.Image
        Water frequency image (0–1 range).
    """
    water_masks = collection.map(lambda img: img.gte(threshold))
    frequency = water_masks.mean().rename('water_frequency')
    return frequency
