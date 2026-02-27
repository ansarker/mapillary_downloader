"""Utility functions for the Mapillary Downloader.

This module contains helper functions for validating bounding boxes 
and other common tasks used across the Mapillary Downloader project.
"""
def validate_bbox(bbox: str) -> list[float] | bool:
    """Validate and parse a bbox string.

    Args:
        bbox: A string in the format 'min_lon,min_lat,max_lon,max_lat'.
    Returns:
        A list of floats representing the bounding box coordinates.
    """
    try:
        min_lon, min_lat, max_lon, max_lat = map(float, bbox.split(","))
        return (min_lon < max_lon) and (min_lat < max_lat)
    except:
        return False
