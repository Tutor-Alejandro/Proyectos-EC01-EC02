"""
Utility functions for Earth Engine operations and general helpers.
"""

import ee
import time
from typing import Dict, List, Optional, Any


class EarthEngineUtils:
    """
    Utility class for common Earth Engine operations.
    """
    
    @staticmethod
    def authenticate_and_initialize(project_id: str, authenticate: bool = False) -> bool:
        """
        Authenticate and initialize Google Earth Engine.
        
        Args:
            project_id: Google Cloud Project ID
            authenticate: Whether to run authentication (first time only)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if authenticate:
                ee.Authenticate()
            
            ee.Initialize(project=project_id)
            return True
            
        except Exception as e:
            print(f"Error initializing Earth Engine: {e}")
            print("Troubleshooting steps:")
            print("1. Run 'earthengine authenticate' in terminal")
            print("2. Verify your project ID is correct")
            print("3. Check your Earth Engine permissions")
            return False
    
    @staticmethod
    def check_initialization() -> bool:
        """
        Check if Earth Engine is initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        try:
            # Try a simple operation to test initialization
            ee.Number(1).getInfo()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a specific Earth Engine task.
        
        Args:
            task_id: Task ID string
            
        Returns:
            Task status dictionary or None if not found
        """
        try:
            tasks = ee.batch.Task.list()
            for task in tasks:
                if task.id == task_id:
                    return task.status()
            return None
        except Exception as e:
            print(f"Error getting task status: {e}")
            return None
    
    @staticmethod
    def cancel_task(task_id: str) -> bool:
        """
        Cancel a specific Earth Engine task.
        
        Args:
            task_id: Task ID string
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        try:
            tasks = ee.batch.Task.list()
            for task in tasks:
                if task.id == task_id:
                    task.cancel()
                    return True
            print(f"Task {task_id} not found")
            return False
        except Exception as e:
            print(f"Error cancelling task: {e}")
            return False
    
    @staticmethod
    def list_running_tasks() -> List[Dict[str, Any]]:
        """
        Get list of currently running tasks.
        
        Returns:
            List of running task information
        """
        try:
            tasks = ee.batch.Task.list()
            running_tasks = []
            
            for task in tasks:
                status = task.status()
                if status['state'] in ['RUNNING', 'READY']:
                    task_info = {
                        'id': task.id,
                        'description': task.config.get('description', 'No description'),
                        'state': status['state'],
                        'creation_timestamp': status.get('creation_timestamp_ms', 0),
                        'update_timestamp': status.get('update_timestamp_ms', 0)
                    }
                    if 'progress' in status:
                        task_info['progress'] = status['progress']
                    
                    running_tasks.append(task_info)
            
            return running_tasks
            
        except Exception as e:
            print(f"Error listing running tasks: {e}")
            return []
    
    @staticmethod
    def cleanup_failed_tasks(max_age_hours: int = 24) -> int:
        """
        Cancel old failed or cancelled tasks.
        
        Args:
            max_age_hours: Maximum age in hours for tasks to keep
            
        Returns:
            Number of tasks cleaned up
        """
        try:
            tasks = ee.batch.Task.list()
            current_time = time.time() * 1000  # Convert to milliseconds
            max_age_ms = max_age_hours * 60 * 60 * 1000
            
            cleaned_count = 0
            
            for task in tasks:
                status = task.status()
                
                # Skip running or completed tasks
                if status['state'] in ['RUNNING', 'READY', 'COMPLETED']:
                    continue
                
                # Check age
                update_time = status.get('update_timestamp_ms', 0)
                if current_time - update_time > max_age_ms:
                    try:
                        task.cancel()
                        cleaned_count += 1
                    except Exception:
                        pass  # Task might already be cancelled
            
            return cleaned_count
            
        except Exception as e:
            print(f"Error cleaning up tasks: {e}")
            return 0


class TaskMonitor:
    """
    Helper class to monitor Earth Engine task progress.
    """
    
    def __init__(self, task: ee.batch.Task, check_interval: int = 30):
        """
        Initialize task monitor.
        
        Args:
            task: Earth Engine task to monitor
            check_interval: Seconds between status checks
        """
        self.task = task
        self.check_interval = check_interval
        self.start_time = time.time()
    
    def monitor(self, verbose: bool = True) -> bool:
        """
        Monitor task until completion.
        
        Args:
            verbose: Whether to print progress updates
            
        Returns:
            True if task completed successfully, False otherwise
        """
        if verbose:
            print(f"Monitoring task: {self.task.id}")
        
        try:
            while self.task.active():
                status = self.task.status()
                state = status['state']
                
                if verbose:
                    elapsed = time.time() - self.start_time
                    print(f"Status: {state} (elapsed: {elapsed:.0f}s)")
                    
                    if 'progress' in status:
                        progress = status['progress']
                        print(f"Progress: {progress}%")
                
                time.sleep(self.check_interval)
            
            final_status = self.task.status()
            final_state = final_status['state']
            
            if verbose:
                total_time = time.time() - self.start_time
                print(f"Task completed: {final_state} (total time: {total_time:.0f}s)")
            
            if final_state == 'COMPLETED':
                return True
            elif final_state == 'FAILED':
                error_msg = final_status.get('error_message', 'Unknown error')
                if verbose:
                    print(f"Task failed: {error_msg}")
                return False
                
        except KeyboardInterrupt:
            if verbose:
                print("Monitoring stopped (task continues running)")
            return False
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current task status.
        
        Returns:
            Status dictionary
        """
        return self.task.status()
    
    def cancel(self) -> bool:
        """
        Cancel the monitored task.
        
        Returns:
            True if cancelled successfully, False otherwise
        """
        try:
            self.task.cancel()
            return True
        except Exception as e:
            print(f"Error cancelling task: {e}")
            return False


def format_file_size(size_mb: float) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_mb: Size in megabytes
        
    Returns:
        Formatted size string
    """
    if size_mb < 1:
        return f"{size_mb * 1024:.1f} KB"
    elif size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb / 1024:.1f} GB"


def format_area(area_km2: float) -> str:
    """
    Format area in human readable format.
    
    Args:
        area_km2: Area in square kilometers
        
    Returns:
        Formatted area string
    """
    if area_km2 < 1:
        return f"{area_km2 * 1000000:.0f} m²"
    elif area_km2 < 10000:
        return f"{area_km2:.1f} km²"
    else:
        return f"{area_km2:,.0f} km²"


def validate_coordinates(west: float, east: float, south: float, north: float) -> bool:
    """
    Validate geographic coordinates.
    
    Args:
        west: Western longitude boundary
        east: Eastern longitude boundary
        south: Southern latitude boundary
        north: Northern latitude boundary
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    # Check longitude ranges
    if not (-180 <= west <= 180) or not (-180 <= east <= 180):
        return False
    
    # Check latitude ranges
    if not (-90 <= south <= 90) or not (-90 <= north <= 90):
        return False
    
    # Check logical constraints
    if west >= east or south >= north:
        return False
    
    return True