"""
Core downloader module for satellite embeddings from Google Earth Engine.
"""

import ee
import os
import time
from typing import Dict, Optional, Any
from datetime import datetime


class SatelliteEmbeddingsDownloader:
    """
    Main class for downloading satellite embeddings from Google Earth Engine.
    """
    
    DATASET_ID = 'GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL'
    DEFAULT_SCALE = 10  # meters per pixel
    DEFAULT_YEAR = 2024
    
    def __init__(self, project_id: str, year: int = DEFAULT_YEAR, scale: int = DEFAULT_SCALE):
        """
        Initialize the downloader.
        
        Args:
            project_id: Google Cloud Project ID
            year: Year for the embeddings data (2017 onwards)
            scale: Resolution in meters per pixel
        """
        self.project_id = project_id
        self.year = year
        self.scale = scale
        self._initialized = False
        
    def initialize(self, authenticate: bool = False) -> bool:
        """
        Initialize Google Earth Engine.
        
        Args:
            authenticate: Whether to run authentication (first time only)
            
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if authenticate:
                ee.Authenticate()
            
            ee.Initialize(project=self.project_id)
            self._initialized = True
            return True
            
        except Exception as e:
            print(f"Error initializing Earth Engine: {e}")
            return False
    
    def get_dataset_info(self, region_bounds: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """
        Get information about the satellite embeddings dataset for a region.
        
        Args:
            region_bounds: Dictionary with 'west', 'east', 'south', 'north' keys
            
        Returns:
            Dataset information dictionary or None if error
        """
        if not self._initialized:
            raise RuntimeError("Earth Engine not initialized. Call initialize() first.")
            
        try:
            geometry = ee.Geometry.Rectangle([
                region_bounds['west'], region_bounds['south'],
                region_bounds['east'], region_bounds['north']
            ])
            
            embeddings = ee.ImageCollection(self.DATASET_ID)
            start_date = ee.Date.fromYMD(self.year, 1, 1)
            end_date = start_date.advance(1, 'year')
            
            filtered_embeddings = embeddings.filter(
                ee.Filter.date(start_date, end_date)
            ).filter(ee.Filter.bounds(geometry))
            
            embeddings_image = filtered_embeddings.mosaic()
            info = embeddings_image.getInfo()
            
            # Calculate area and estimated size
            area_km2 = geometry.area().getInfo() / 1e6
            num_pixels = area_km2 * 1e6 / (self.scale * self.scale)
            size_mb = (num_pixels * 64 * 4) / 1e6  # 64 bands, 4 bytes per float32
            
            return {
                'dataset_id': self.DATASET_ID,
                'year': self.year,
                'scale': self.scale,
                'num_bands': len(info['bands']),
                'band_names': [band['id'] for band in info['bands']],
                'area_km2': area_km2,
                'estimated_pixels': int(num_pixels),
                'estimated_size_mb': int(size_mb)
            }
            
        except Exception as e:
            print(f"Error getting dataset info: {e}")
            return None
    
    def download_to_drive(self, region_bounds: Dict[str, float], 
                         description: str = None,
                         folder: str = 'EarthEngine_Exports') -> Optional[ee.batch.Task]:
        """
        Download satellite embeddings to Google Drive.
        
        Args:
            region_bounds: Dictionary with 'west', 'east', 'south', 'north' keys
            description: Task description (auto-generated if None)
            folder: Google Drive folder name
            
        Returns:
            Earth Engine task object or None if error
        """
        if not self._initialized:
            raise RuntimeError("Earth Engine not initialized. Call initialize() first.")
            
        if description is None:
            description = f'satellite_embeddings_{self.year}'
            
        try:
            geometry = ee.Geometry.Rectangle([
                region_bounds['west'], region_bounds['south'],
                region_bounds['east'], region_bounds['north']
            ])
            
            embeddings = ee.ImageCollection(self.DATASET_ID)
            start_date = ee.Date.fromYMD(self.year, 1, 1)
            end_date = start_date.advance(1, 'year')
            
            filtered_embeddings = embeddings.filter(
                ee.Filter.date(start_date, end_date)
            ).filter(ee.Filter.bounds(geometry))
            
            embeddings_image = filtered_embeddings.mosaic().clip(geometry)
            
            task = ee.batch.Export.image.toDrive(
                image=embeddings_image,
                description=description,
                folder=folder,
                fileNamePrefix=description,
                scale=self.scale,
                region=geometry,
                maxPixels=1e13,
                fileFormat='GeoTIFF'
            )
            
            task.start()
            return task
            
        except Exception as e:
            print(f"Error starting download: {e}")
            return None
    
    def download_to_asset(self, region_bounds: Dict[str, float],
                         asset_id: str,
                         description: str = None) -> Optional[ee.batch.Task]:
        """
        Download satellite embeddings to Earth Engine Asset.
        
        Args:
            region_bounds: Dictionary with 'west', 'east', 'south', 'north' keys
            asset_id: Full asset ID path
            description: Task description (auto-generated if None)
            
        Returns:
            Earth Engine task object or None if error
        """
        if not self._initialized:
            raise RuntimeError("Earth Engine not initialized. Call initialize() first.")
            
        if description is None:
            description = f'satellite_embeddings_asset_{self.year}'
            
        try:
            geometry = ee.Geometry.Rectangle([
                region_bounds['west'], region_bounds['south'],
                region_bounds['east'], region_bounds['north']
            ])
            
            embeddings = ee.ImageCollection(self.DATASET_ID)
            start_date = ee.Date.fromYMD(self.year, 1, 1)
            end_date = start_date.advance(1, 'year')
            
            filtered_embeddings = embeddings.filter(
                ee.Filter.date(start_date, end_date)
            ).filter(ee.Filter.bounds(geometry))
            
            embeddings_image = filtered_embeddings.mosaic().clip(geometry)
            
            task = ee.batch.Export.image.toAsset(
                image=embeddings_image,
                description=description,
                assetId=asset_id,
                scale=self.scale,
                region=geometry,
                maxPixels=1e13
            )
            
            task.start()
            return task
            
        except Exception as e:
            print(f"Error starting asset export: {e}")
            return None
    
    @staticmethod
    def monitor_task(task: ee.batch.Task, check_interval: int = 30) -> bool:
        """
        Monitor the progress of an Earth Engine task.
        
        Args:
            task: Earth Engine task object
            check_interval: Seconds between status checks
            
        Returns:
            True if task completed successfully, False otherwise
        """
        print(f"Monitoring task: {task.id}")
        
        try:
            while task.active():
                status = task.status()
                state = status['state']
                print(f"Status: {state}")
                
                if 'progress' in status:
                    progress = status['progress']
                    print(f"Progress: {progress}%")
                
                time.sleep(check_interval)
            
            final_status = task.status()
            final_state = final_status['state']
            print(f"Task completed: {final_state}")
            
            if final_state == 'COMPLETED':
                return True
            elif final_state == 'FAILED':
                error_msg = final_status.get('error_message', 'Unknown error')
                print(f"Task failed: {error_msg}")
                return False
                
        except KeyboardInterrupt:
            print("Monitoring stopped (task continues running)")
            return False
            
        return False
    
    @staticmethod
    def list_tasks(limit: int = 10) -> None:
        """
        List recent Earth Engine tasks.
        
        Args:
            limit: Maximum number of tasks to show
        """
        try:
            tasks = ee.batch.Task.list()[:limit]
            
            if not tasks:
                print("No tasks found")
                return
                
            print(f"Recent tasks ({len(tasks)}):")
            for task in tasks:
                status = task.status()
                state = status['state']
                description = task.config.get('description', 'No description')
                print(f"- {description}: {state}")
                
        except Exception as e:
            print(f"Error listing tasks: {e}")