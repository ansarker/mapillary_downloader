# Mapillary Image Downloader

A Python package to download Mapillary images using their API.

## Installation

```bash
git clone https://github.com/ansarker/mapillary-downloader.git
cd mapillary-downloader
pip install -e .
```

## Usage

### Download images in a bounding box
```python
from mapillary_downloader.downloader import MapillaryDownloader

downloader = MapillaryDownloader("YOUR_ACCESS_TOKEN")
image_ids = downloader.get_images_in_bbox("min_lon,min_lat,max_lon,max_lat")

for img_id in image_ids:
    downloader.download_image(img_id, output_dir="./downloads")
```

## Command Line Interface

### Basic Usage
```bash
mapillary-download \
    --token "MLY|YOUR_ACCESS_TOKEN" \
    --bbox "min_lon,min_lat,max_lon,max_lat" \
    --output ./downloads
```

### Advanced Options
```bash
mapillary-download \
    --token "MLY|YOUR_TOKEN" \
    --bbox "90.363,23.805,90.368,23.807" \
    --output ./my_images \
    --limit 100  # Only download first 100 images
```

### Help Menu
```bash
mapillary-download --help
```

## Configuration
1. Get your access token from [Mapillary Developer Dashboard](https://www.mapillary.com/dashboard/developers)
2. Format bbox as `min_lon,min_lat,max_lon,max_lat`

## License
MIT