# TopogenTech Library

A modular Python library for downloading satellite embeddings from Google Earth Engine.

## Installation

```bash
# Install from source
pip install -e .

# Or install with development dependencies
pip install -e .[dev]
```

## Basic Usage

```python
from topogentech import SatelliteEmbeddingsDownloader, RegionConfig

# Initialize downloader
downloader = SatelliteEmbeddingsDownloader(project_id='your-gcp-project-id')

# Initialize Earth Engine
downloader.initialize()

# Get region bounds
ecuador_bounds = RegionConfig.get_country_bounds('ecuador')

# Download to Google Drive
task = downloader.download_to_drive(
    region_bounds=ecuador_bounds,
    description='ecuador_embeddings_2024'
)

print(f"Download started: {task.id}")
```

## Available Regions

The library includes predefined boundaries for:

**Countries**: ecuador, colombia, peru, brazil, bolivia, chile, argentina, venezuela, and more

**Cities**: quito, guayaquil, cuenca, bogota, lima, santiago, and more

## Features

- Clean, modular API
- Predefined region boundaries
- Support for custom regions
- Task monitoring and management
- Export to Google Drive or Earth Engine Assets
- Type hints and comprehensive documentation

## Requirements

- Python 3.8+
- Google Earth Engine account
- Google Cloud Project with Earth Engine API enabled

See `examples/basic_usage.py` for complete examples.