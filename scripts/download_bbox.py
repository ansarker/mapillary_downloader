import argparse
from pathlib import Path
from mapillary_downloader.downloader import MapillaryDownloader

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download Mapillary images within a bounding box"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="Mapillary API access token (required)"
    )
    parser.add_argument(
        "--bbox",
        required=True,
        help="Bounding box as 'min_lon,min_lat,max_lon,max_lat'"
    )
    parser.add_argument(
        "--output",
        default="./downloads",
        help="Output directory (default: ./downloads)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of images to download"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    downloader = MapillaryDownloader(args.token)
    print(f"Fetching images in bbox: {args.bbox}")
    
    try:
        image_ids = downloader.get_images_in_bbox(args.bbox)
        if args.limit:
            image_ids = image_ids[:args.limit]
        
        print(f"Found {len(image_ids)} images. Downloading...")
        
        for img_id in image_ids:
            downloader.download_image(img_id, output_dir=args.output)
            
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()