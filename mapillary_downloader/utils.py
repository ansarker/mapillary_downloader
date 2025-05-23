from typing import Tuple

def validate_bbox(bbox: str) -> Tuple[float, float, float, float]:
    """Validate and parse a bbox string."""
    try:
        min_lon, min_lat, max_lon, max_lat = map(float, bbox.split(","))
        return (min_lon < max_lon) and (min_lat < max_lat)
    except:
        return False
