# Collect GPS

This script extracts GPS coordinates from images and saves them to a CSV file. 

## Inputs

The input is a directory path containing GeoTIFF images that contain georeferencing metadata.

## Outputs

## Arguments and Flags
* **Positional Arguments:** 
    * **Directory containing files to process:** 'dir' 
* **Required Arguments:**
    * **Scan date:** '-sd', '--scandate'
                
* **Optional Arguments:**
    * **Output directory:** '-o', '--outdir', default='img_coords_out/'
