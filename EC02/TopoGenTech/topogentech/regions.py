"""
Region configuration module with predefined bounding boxes for countries and cities.
"""

from typing import Dict, List, Optional


class RegionConfig:
    """
    Configuration class for managing geographic regions and their bounding boxes.
    """
    
    # Predefined country boundaries
    COUNTRIES = {
        'ecuador': {
            'west': -81.5,
            'east': -75.0,
            'south': -5.0,
            'north': 2.0,
            'name': 'Ecuador'
        },
        'colombia': {
            'west': -81.8,
            'east': -66.9,
            'south': -4.2,
            'north': 15.5,
            'name': 'Colombia'
        },
        'peru': {
            'west': -84.6,
            'east': -68.7,
            'south': -18.4,
            'north': -0.1,
            'name': 'Peru'
        },
        'brazil': {
            'west': -73.9,
            'east': -28.8,
            'south': -33.8,
            'north': 5.3,
            'name': 'Brazil'
        },
        'bolivia': {
            'west': -69.6,
            'east': -57.5,
            'south': -22.9,
            'north': -9.7,
            'name': 'Bolivia'
        },
        'chile': {
            'west': -75.6,
            'east': -66.4,
            'south': -55.6,
            'north': -17.5,
            'name': 'Chile'
        },
        'argentina': {
            'west': -73.6,
            'east': -53.6,
            'south': -55.1,
            'north': -21.8,
            'name': 'Argentina'
        },
        'venezuela': {
            'west': -73.4,
            'east': -59.8,
            'south': 0.6,
            'north': 15.7,
            'name': 'Venezuela'
        },
        'guyana': {
            'west': -61.4,
            'east': -56.5,
            'south': 1.2,
            'north': 8.6,
            'name': 'Guyana'
        },
        'suriname': {
            'west': -58.1,
            'east': -53.9,
            'south': 1.8,
            'north': 6.0,
            'name': 'Suriname'
        },
        'french_guiana': {
            'west': -54.6,
            'east': -51.6,
            'south': 2.1,
            'north': 5.8,
            'name': 'French Guiana'
        },
        'paraguay': {
            'west': -62.6,
            'east': -54.3,
            'south': -27.6,
            'north': -19.3,
            'name': 'Paraguay'
        },
        'uruguay': {
            'west': -58.4,
            'east': -53.1,
            'south': -35.0,
            'north': -30.1,
            'name': 'Uruguay'
        }
    }
    
    # Predefined city boundaries (smaller test regions)
    CITIES = {
        'quito': {
            'west': -78.6,
            'east': -78.4,
            'south': -0.3,
            'north': -0.1,
            'name': 'Quito, Ecuador',
            'country': 'ecuador'
        },
        'guayaquil': {
            'west': -80.1,
            'east': -79.8,
            'south': -2.3,
            'north': -2.0,
            'name': 'Guayaquil, Ecuador',
            'country': 'ecuador'
        },
        'cuenca': {
            'west': -79.0,
            'east': -78.9,
            'south': -2.9,
            'north': -2.8,
            'name': 'Cuenca, Ecuador',
            'country': 'ecuador'
        },
        'bogota': {
            'west': -74.2,
            'east': -74.0,
            'south': 4.5,
            'north': 4.8,
            'name': 'Bogota, Colombia',
            'country': 'colombia'
        },
        'medellin': {
            'west': -75.6,
            'east': -75.5,
            'south': 6.2,
            'north': 6.3,
            'name': 'Medellin, Colombia',
            'country': 'colombia'
        },
        'lima': {
            'west': -77.2,
            'east': -76.9,
            'south': -12.2,
            'north': -11.9,
            'name': 'Lima, Peru',
            'country': 'peru'
        },
        'sao_paulo': {
            'west': -46.8,
            'east': -46.4,
            'south': -23.7,
            'north': -23.4,
            'name': 'São Paulo, Brazil',
            'country': 'brazil'
        },
        'rio_de_janeiro': {
            'west': -43.8,
            'east': -43.1,
            'south': -23.1,
            'north': -22.8,
            'name': 'Rio de Janeiro, Brazil',
            'country': 'brazil'
        },
        'buenos_aires': {
            'west': -58.5,
            'east': -58.3,
            'south': -34.7,
            'north': -34.5,
            'name': 'Buenos Aires, Argentina',
            'country': 'argentina'
        },
        'santiago': {
            'west': -70.8,
            'east': -70.5,
            'south': -33.6,
            'north': -33.3,
            'name': 'Santiago, Chile',
            'country': 'chile'
        },
        'caracas': {
            'west': -67.0,
            'east': -66.8,
            'south': 10.4,
            'north': 10.6,
            'name': 'Caracas, Venezuela',
            'country': 'venezuela'
        },
        'la_paz': {
            'west': -68.2,
            'east': -68.0,
            'south': -16.6,
            'north': -16.4,
            'name': 'La Paz, Bolivia',
            'country': 'bolivia'
        }
    }
    
    @classmethod
    def get_country_bounds(cls, country_name: str) -> Optional[Dict[str, float]]:
        """
        Get bounding box for a country.
        
        Args:
            country_name: Name of the country (lowercase)
            
        Returns:
            Dictionary with bounding box coordinates or None if not found
        """
        return cls.COUNTRIES.get(country_name.lower())
    
    @classmethod
    def get_city_bounds(cls, city_name: str) -> Optional[Dict[str, float]]:
        """
        Get bounding box for a city.
        
        Args:
            city_name: Name of the city (lowercase)
            
        Returns:
            Dictionary with bounding box coordinates or None if not found
        """
        return cls.CITIES.get(city_name.lower())
    
    @classmethod
    def get_region_bounds(cls, region_name: str) -> Optional[Dict[str, float]]:
        """
        Get bounding box for any region (country or city).
        
        Args:
            region_name: Name of the region (lowercase)
            
        Returns:
            Dictionary with bounding box coordinates or None if not found
        """
        # Try cities first (more specific)
        bounds = cls.get_city_bounds(region_name)
        if bounds:
            return bounds
            
        # Then try countries
        return cls.get_country_bounds(region_name)
    
    @classmethod
    def list_available_countries(cls) -> List[str]:
        """
        Get list of available country names.
        
        Returns:
            List of country names
        """
        return list(cls.COUNTRIES.keys())
    
    @classmethod
    def list_available_cities(cls) -> List[str]:
        """
        Get list of available city names.
        
        Returns:
            List of city names
        """
        return list(cls.CITIES.keys())
    
    @classmethod
    def list_all_regions(cls) -> Dict[str, List[str]]:
        """
        Get all available regions organized by type.
        
        Returns:
            Dictionary with 'countries' and 'cities' keys
        """
        return {
            'countries': cls.list_available_countries(),
            'cities': cls.list_available_cities()
        }
    
    @classmethod
    def create_custom_bounds(cls, west: float, east: float, 
                           south: float, north: float, 
                           name: str = "Custom Region") -> Dict[str, float]:
        """
        Create a custom bounding box.
        
        Args:
            west: Western longitude boundary
            east: Eastern longitude boundary
            south: Southern latitude boundary
            north: Northern latitude boundary
            name: Name for the region
            
        Returns:
            Dictionary with bounding box coordinates
        """
        return {
            'west': west,
            'east': east,
            'south': south,
            'north': north,
            'name': name
        }
    
    @classmethod
    def validate_bounds(cls, bounds: Dict[str, float]) -> bool:
        """
        Validate that bounding box coordinates are reasonable.
        
        Args:
            bounds: Dictionary with bounding box coordinates
            
        Returns:
            True if bounds are valid, False otherwise
        """
        required_keys = ['west', 'east', 'south', 'north']
        
        # Check if all required keys are present
        if not all(key in bounds for key in required_keys):
            return False
        
        # Check coordinate ranges
        if not (-180 <= bounds['west'] <= 180):
            return False
        if not (-180 <= bounds['east'] <= 180):
            return False
        if not (-90 <= bounds['south'] <= 90):
            return False
        if not (-90 <= bounds['north'] <= 90):
            return False
        
        # Check logical constraints
        if bounds['west'] >= bounds['east']:
            return False
        if bounds['south'] >= bounds['north']:
            return False
        
        return True
    
    @classmethod
    def get_bounds_info(cls, bounds: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate area and other information for a bounding box.
        
        Args:
            bounds: Dictionary with bounding box coordinates
            
        Returns:
            Dictionary with calculated information
        """
        if not cls.validate_bounds(bounds):
            raise ValueError("Invalid bounding box coordinates")
        
        # Approximate area calculation (not perfect due to Earth's curvature)
        width_deg = bounds['east'] - bounds['west']
        height_deg = bounds['north'] - bounds['south']
        
        # Convert to approximate km (very rough calculation)
        width_km = width_deg * 111.32  # degrees to km at equator
        height_km = height_deg * 110.54  # degrees to km
        area_km2 = width_km * height_km
        
        return {
            'width_degrees': width_deg,
            'height_degrees': height_deg,
            'width_km': width_km,
            'height_km': height_km,
            'area_km2': area_km2,
            'center_lon': (bounds['west'] + bounds['east']) / 2,
            'center_lat': (bounds['south'] + bounds['north']) / 2
        }