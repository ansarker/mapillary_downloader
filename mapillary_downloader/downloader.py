import json
import os
import requests
from mapillary_downloader.utils import validate_bbox

class MapillaryDownloader:
    """A class to download Mapillary images using their API."""
    
    BASE_API_URL = "https://graph.mapillary.com"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        
    def _make_api_request(self, endpoint: str, params: dict | None = None) -> dict:
        """Helper method to make API requests.
        Args:
            endpoint: The API endpoint to call (e.g., 'images').
            params: Optional query parameters for the API call.
        Returns:
            The JSON response from the API as a dictionary.
        Raises:
            requests.HTTPError: If the API request fails.
        """
        url = f"{self.BASE_API_URL}/{endpoint}"
        params = params or {}
        params.setdefault("access_token", self.access_token)
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_images_in_bbox(self, bbox: str, fields: str = "id") -> list[str]:
        """Fetch image IDs within a bounding box.
        Args:
            bbox: Bounding box in the format 'min_lon,min_lat,max_lon,max_lat'.
            fields: Comma-separated list of fields to return (default: 'id').
        Returns:
            A list of image IDs found within the bounding box.
        """
        assert validate_bbox(bbox), "Invalid bbox! First two lat, long need to be smaller than the next lat, long"
        params = {
            "bbox": bbox,
            "fields": fields
        }
        data = self._make_api_request("images", params)
        return [img["id"] for img in data["data"]]
    
    def get_images_by_user_in_bbox(self, username: str, bbox: str, fields: str = "id") -> list[str]:
        """Fetch image IDs by a specific user within a bounding box.
        Args:
            username: The Mapillary username to filter by.
            bbox: Bounding box in the format 'min_lon,min_lat,max_lon,max_lat'.
            fields: Comma-separated list of fields to return (default: 'id').
        Returns:
            A list of image IDs found for the user within the bounding box.
        """
        assert validate_bbox(bbox), "Invalid bbox! First two lat, long need to be smaller than the next lat, long"
        params = {
            "creator_username": username,
            "bbox": bbox,
            "fields": fields,
        }

        data = self._make_api_request("images", params)
        print('Username datas: ', data)
        return [img["id"] for img in data["data"]]
    
    def download_image(self, image_id: str, output_dir: str = ".") -> None:
        """Download a single image by ID.
        
        This method fetches the image metadata, downloads the image, and saves it to the specified directory. 
        It also extracts GPS coordinates and capture time from the metadata and saves this information to a CSV file.
        
        Args:
            image_id: The ID of the image to download.
            output_dir: The directory where the image and metadata will be saved.        
        """
        output_images_dir = f"{output_dir}/images"
        output_jsons_dir = f"{output_dir}/jsons"
        
        # Create directories if they don't exist
        for dir_path in [output_images_dir, output_jsons_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
        
        fields = (
            "thumb_original_url,"
            "computed_geometry,"
            "captured_at,"
            "computed_compass_angle,"
            "camera_parameters,"
            "computed_rotation,"
            "camera_type"
        )
        metadata = self._make_api_request(
            endpoint=image_id,
            params={"fields": fields}
        )
        
        if "thumb_original_url" not in metadata:
            raise ValueError(f"No image found for ID: {image_id}")
            
        image_url = metadata["thumb_original_url"]
        image_data = self.session.get(image_url).content
        
        with open(os.path.join(output_images_dir, f"{image_id}.jpg"), "wb") as f:
            f.write(image_data)
            
        # Extract coordinates to match your existing JSON structure
        coords = metadata.get("computed_geometry", {}).get("coordinates", [0, 0])
        
        json_data = {
            "image_name": f"{image_id}.jpg",
            "latitude": coords[1],
            "longitude": coords[0],
            "captured_at": metadata.get("captured_at"),
            "heading": metadata.get("computed_compass_angle"),
            "camera_parameters": metadata.get("camera_parameters"),
            "camera_type": metadata.get("camera_type"),
            "computed_rotation": metadata.get("computed_rotation"),
            "annotations": []
        }
        
        with open(os.path.join(output_jsons_dir, f"{image_id}.json"), "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"Downloaded image and metadata for: {image_id}")