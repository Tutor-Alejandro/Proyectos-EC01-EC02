#!/usr/bin/env python3
"""
Example usage of the TopogenTech Satellite Embeddings Downloader library.

This script demonstrates how to use the library to download satellite embeddings
for different regions using Google Earth Engine.
"""

from topogentech import SatelliteEmbeddingsDownloader, RegionConfig, EarthEngineUtils


def main():
    """Main example function."""
    
    # Configuration
    PROJECT_ID = 'your-gcp-project-id'  # Replace with your actual project ID
    YEAR = 2024
    SCALE = 10  # meters per pixel
    
    print("TopogenTech Satellite Embeddings Downloader Example")
    print("=" * 55)
    
    # Initialize the downloader
    downloader = SatelliteEmbeddingsDownloader(
        project_id=PROJECT_ID,
        year=YEAR,
        scale=SCALE
    )
    
    # Initialize Earth Engine (set authenticate=True for first time)
    print("Initializing Google Earth Engine...")
    if not downloader.initialize(authenticate=False):
        print("Failed to initialize Earth Engine. Please check your configuration.")
        return
    
    print("Earth Engine initialized successfully!")
    
    # Example 1: List available regions
    print("\nAvailable regions:")
    regions = RegionConfig.list_all_regions()
    print(f"Countries: {', '.join(regions['countries'][:5])}... ({len(regions['countries'])} total)")
    print(f"Cities: {', '.join(regions['cities'][:5])}... ({len(regions['cities'])} total)")
    
    # Example 2: Get region information
    print("\nRegion information:")
    
    # Get bounds for Ecuador
    ecuador_bounds = RegionConfig.get_country_bounds('ecuador')
    if ecuador_bounds:
        print(f"Ecuador bounds: {ecuador_bounds}")
        
        # Get dataset information for Ecuador
        info = downloader.get_dataset_info(ecuador_bounds)
        if info:
            print(f"Dataset info for Ecuador:")
            print(f"  - Bands: {info['num_bands']}")
            print(f"  - Area: {info['area_km2']:.0f} km²")
            print(f"  - Estimated size: {info['estimated_size_mb']:.0f} MB")
    
    # Example 3: Download small test region (Quito)
    print("\nDownloading test region (Quito)...")
    
    quito_bounds = RegionConfig.get_city_bounds('quito')
    if quito_bounds:
        print(f"Quito bounds: {quito_bounds}")
        
        # Start download task
        task = downloader.download_to_drive(
            region_bounds=quito_bounds,
            description='quito_embeddings_test',
            folder='EarthEngine_Exports'
        )
        
        if task:
            print(f"Download task started: {task.id}")
            print("Files will be available in Google Drive > EarthEngine_Exports")
            
            # Optional: Monitor progress
            choice = input("Monitor progress? (y/n): ").strip().lower()
            if choice == 'y':
                success = downloader.monitor_task(task)
                if success:
                    print("Download completed successfully!")
                else:
                    print("Download failed or was interrupted")
        else:
            print("Failed to start download task")
    
    # Example 4: Custom region
    print("\nCustom region example:")
    
    # Create custom bounds for a small area
    custom_bounds = RegionConfig.create_custom_bounds(
        west=-78.5,
        east=-78.4,
        south=-0.2,
        north=-0.1,
        name="Custom Test Area"
    )
    
    print(f"Custom bounds: {custom_bounds}")
    
    # Validate bounds
    if RegionConfig.validate_bounds(custom_bounds):
        print("Custom bounds are valid")
        
        # Get bounds information
        bounds_info = RegionConfig.get_bounds_info(custom_bounds)
        print(f"Area: {bounds_info['area_km2']:.2f} km²")
        print(f"Center: ({bounds_info['center_lat']:.3f}, {bounds_info['center_lon']:.3f})")
    
    # Example 5: List current tasks
    print("\nCurrent Earth Engine tasks:")
    downloader.list_tasks(limit=5)
    
    print("\nExample completed!")
    print("\nNext steps:")
    print("1. Replace 'your-gcp-project-id' with your actual GCP project ID")
    print("2. Set authenticate=True for first-time setup")
    print("3. Choose your region and run the download")
    print("4. Check Google Drive > EarthEngine_Exports for downloaded files")


def simple_download_example():
    """Simple example for quick downloads."""
    
    # Quick setup
    PROJECT_ID = 'your-gcp-project-id'
    
    # Initialize downloader
    downloader = SatelliteEmbeddingsDownloader(project_id=PROJECT_ID)
    
    # Initialize Earth Engine
    if not downloader.initialize():
        print("Failed to initialize Earth Engine")
        return
    
    # Download Ecuador embeddings
    ecuador_bounds = RegionConfig.get_country_bounds('ecuador')
    
    if ecuador_bounds:
        task = downloader.download_to_drive(
            region_bounds=ecuador_bounds,
            description='ecuador_embeddings_2024'
        )
        
        if task:
            print(f"Download started: {task.id}")
            print("Check Google Drive > EarthEngine_Exports for your files")
        else:
            print("Download failed to start")


def city_download_example():
    """Example for downloading city-level embeddings."""
    
    PROJECT_ID = 'your-gcp-project-id'
    
    # Available cities
    cities = ['quito', 'guayaquil', 'cuenca', 'bogota', 'lima', 'santiago']
    
    downloader = SatelliteEmbeddingsDownloader(project_id=PROJECT_ID)
    
    if not downloader.initialize():
        print("Failed to initialize Earth Engine")
        return
    
    print("Downloading embeddings for multiple cities...")
    
    for city in cities:
        city_bounds = RegionConfig.get_city_bounds(city)
        
        if city_bounds:
            task = downloader.download_to_drive(
                region_bounds=city_bounds,
                description=f'{city}_embeddings_2024'
            )
            
            if task:
                print(f"Started download for {city}: {task.id}")
            else:
                print(f"Failed to start download for {city}")


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to run other examples:
    # simple_download_example()
    # city_download_example()