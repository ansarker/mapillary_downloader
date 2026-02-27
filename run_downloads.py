"""This script reads bounding box coordinates from a specified input file and runs a download script for each grid defined in the file.

The input file should have the following format (one grid per line):
ID,min_lon,min_lat,max_lon,max_lat

Example:
    grid1,-122.5,37.7,-122.4,37.8

The script uses the MAPILLARY_TOKEN environment variable for authentication and saves the downloaded data in a specified output directory.
"""
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
INPUT_FILE = "downloads/study_area_segments.txt"
TOKEN = os.environ.get('MAPILLARY_TOKEN')
BASE_OUTPUT_DIR = "./downloads"

print(TOKEN)

def run_batch_download():
    """
    Reads the grids from the input file and runs the download script for each grid.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            
            # Parsing: ID, min_lon, min_lat, max_lon, max_lat
            parts = line.strip().split(',')
            grid_id = parts[0]
            bbox = ",".join(parts[1:]) # Recombines the 4 coords into a string
            
            output_path = os.path.join(BASE_OUTPUT_DIR, grid_id)
            
            # Construct the command
            # Note: We keep the limit at 1000, 
            command = [
                "python3", "scripts/download_bbox.py",
                "--token", TOKEN,
                "--bbox", bbox,
                "--output", output_path,
                "--limit", "1000"
            ]
            
            print(f"----- Processing Grid {grid_id} -----")
            print(f"Executing: {' '.join(command)}")
            
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to download grid {grid_id}: {e}")

if __name__ == "__main__":
    run_batch_download()