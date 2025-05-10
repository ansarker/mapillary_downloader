import os
import csv
import requests
from mapillary_downloader.utils import validate_bbox
from typing import List, Optional

class MapillaryDownloader:
    """A class to download Mapillary images using their API."""
    
    BASE_API_URL = "https://graph.mapillary.com"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        
    def _make_api_request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Helper method to make API requests."""
        url = f"{self.BASE_API_URL}/{endpoint}"
        params = params or {}
        params.setdefault("access_token", self.access_token)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_images_in_bbox(self, bbox: str, fields: str = "id") -> List[str]:
        """Fetch image IDs within a bounding box."""
        assert validate_bbox(bbox), "Invalid bbox! First two lat, long need to be smaller than the next lat, long"
        params = {
            "bbox": bbox,
            "fields": fields
        }
        data = self._make_api_request("images", params)
        return [img["id"] for img in data["data"]]
    
    def download_image(self, image_id: str, output_dir: str = ".") -> None:
        """Download a single image by ID."""
        metadata = self._make_api_request(
            endpoint=image_id,
            params={"fields": "thumb_original_url,computed_geometry,captured_at,detections"}
        )
        
        if "thumb_original_url" not in metadata:
            raise ValueError(f"No image found for ID: {image_id}")
            
        image_url = metadata["thumb_original_url"]
        image_data = self.session.get(image_url).content
        
        output_path = f"{output_dir}/{image_id}.jpg"
        with open(output_path, "wb") as f:
            f.write(image_data)
        
        coords = metadata.get("computed_geometry", {}).get("coordinates")
        captured_at = metadata.get("captured_at", "")
        detections = metadata.get("detections", [])

        # Save metadata to CSV
        csv_path = f"{output_dir}/image_locations.csv"
        write_header = not os.path.exists(csv_path)

        with open(csv_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            if write_header:
                writer.writerow(["latitude", "longitude", "image_path", "captured_at", "num_detections"])
            
            if coords and len(coords) == 2:
                longitude, latitude = coords  # GeoJSON order
                writer.writerow([latitude, longitude, output_path, captured_at, len(detections)])
                print(f"Saved metadata: lat={latitude}, lon={longitude}, time={captured_at}, detections={len(detections)}")
            else:
                print(f"No GPS metadata found for {image_id}")
        
        print(f"Downloaded: {output_path}")