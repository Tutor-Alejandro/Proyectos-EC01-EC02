"""
TopogenTech - Satellite Embeddings Downloader Library

A modular library for downloading satellite embeddings from Google Earth Engine.
"""

from .downloader import SatelliteEmbeddingsDownloader
from .regions import RegionConfig
from .utils import EarthEngineUtils

__version__ = "0.1.0"
__author__ = "TopogenTech Team"

__all__ = [
    "SatelliteEmbeddingsDownloader",
    "RegionConfig", 
    "EarthEngineUtils"
]