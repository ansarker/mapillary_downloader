# Mapillary Image Downloader

A specialized Python package and CLI tool designed to download high-resolution street-level imagery from Mapillary, optimized for large-scale geospatial research.

## Installation

### 1. Clone and Navigate

```bash
git clone https://github.com/ansarker/mapillary-downloader.git
cd mapillary-downloader
```

### 2. Environment Setup
It is recommended to use the included virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

## Project Structure
Based on the research workflow, the project is organized as follows:

- `mapillary_downloader/`: Core logic and API wrappers.
- `scripts/`: Implementation scripts (e.g., `download_bbox.py`).
- `downloads/`: Default output directory for image segments, and json metadata.

## Usage

### Command Line Interface (CLI)

**Basic Usage**

```bash
mapillary-download \
    --token "MLY|YOUR_ACCESS_TOKEN" \
    --bbox "min_lon,min_lat,max_lon,max_lat" \
    --output ./downloads
```

### Help Menu
```bash
mapillary-download --help
```

## Batch Processing for Research Grids

To handle API constraints (e.g., the 1,000-image limit per BBOX), the study area should be discretized into grids (1, 2, 3... 19). You can automate the download of multiple segments using a wrapper script:
```bash
python3 run_downloads.py
```

## Python API
For custom integration into your research pipeline:

```Python
from mapillary_downloader.downloader import MapillaryDownloader

# Initialize with Mapillary API Token
downloader = MapillaryDownloader("YOUR_ACCESS_TOKEN")

# Retrieve image IDs within a specific bounding box
image_ids = downloader.get_images_in_bbox("90.408544,23.735530,90.420152,23.744535")

# Download to a specific segment folder
for img_id in image_ids:
    downloader.download_image(img_id, output_dir="./downloads/1")
```

## Research Context: Spatial Discretization
This tool is used to bypass image download quotas by segmenting large study areas into smaller, manageable grids.

- **Standard Grids**: Used for general urban blocks.
- **Refined Segments (e.g., Grid 4, 17)**: Smaller footprints used to focus on high-density street corridors or intersections to stay within the 1,000-image threshold per request.

## Configuration
1. Get your access token from [Mapillary Developer Dashboard](https://www.mapillary.com/dashboard/developers)
2. **BBOX Format**: Ensure coordinates follow the `min_lon,min_lat,max_lon,max_lat` sequence.

## License

MIT

### What changed?
1.  **Added Project Structure:** Explicitly mentioned the `scripts/` folder and `venv` to match your VS Code explorer.
2.  **Added Batch Processing section:** Mentioned `run_downloads.py` since that is now a core part of your workflow for the 19 grids.
3.  **Included Research Context:** Added the section on "Spatial Discretization" so that anyone visiting your repo understands why you have folders like `downloads/4` or `downloads/17`.
4.  **Refined Installation:** Emphasized the `-e .` install, which fixes the `ModuleNotFoundError` you encountered.