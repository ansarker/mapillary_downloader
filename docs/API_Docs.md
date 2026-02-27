# API Documentation: Mapillary Image Downloader
This documentation covers the technical implementation for the automated retrieval of street-level imagery using the `Mapillary API v4`.

---
## Installation

**Using pip**

```bash
pip install git+https://github.com/ansarker/mapillary_downloader.git
```

## 🔧 Core Implementation
The downloader is built to interface with Mapillary's geospatial database to extract high-resolution images based on coordinate boundaries.

### 1. Authentication & Setup

The module utilizes `python-dotenv` for secure credential management. Ensure your `.env` file contains a valid `MAPILLARY_TOKEN`.

```python
import os
from dotenv import load_dotenv
from mapillary_downloader.downloader import MapillaryDownloader

# Load environment variables
load_dotenv()

# Initialize API Client
TOKEN = os.environ.get("MAPILLARY_TOKEN")
downloader = MapillaryDownloader(TOKEN)
```

### 2. Geographic Querying (Bounding Box)

The system identifies images within a rectangular area defined by two sets of coordinates.

Parameter Format: `min_lon, min_lat, max_lon, max_lat`

### 3. Image Acquisition Loop

The downloader iterates through discovered IDs and handles individual request failures to ensure process continuity.

```python
# Search for images in the defined area
image_ids = downloader.get_images_in_bbox(dhaka_bbox)

# Sequential Download with Error Handling
for image_id in image_ids:
    try:
        downloader.download_image(image_id, output_dir="./my_new_downloads")
    except Exception as e:
        # Prevents a single 404/Timeout from breaking the batch
        print(f"Error downloading image {image_id}: {e}")
```

---

## 🛠 Prerequisites
Ensure the following packages are installed in your environment:
- `python-dotenv`: For environment variable management.
`mapillary-downloader`: The core API wrapper.

### ⚠️ Known Constraints
- **Coordinate Order**: The API strictly requires Longitude before Latitude. Reversing these will result in zero results or incorrect regions.
- **Rate Limiting**: Excessive concurrent requests may be throttled. The current implementation uses a sequential loop to remain within safe limits.
- **Disk Space**: High-resolution imagery can be large. Ensure the destination directory has adequate overhead.

---

**Release Version**: 0.1.0