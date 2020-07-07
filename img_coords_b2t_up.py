#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez
Date   : 2020-03-25
Purpose: Generate a CSV file with GPS coordinates for various points of gantry images.
"""

import argparse
import os
import sys
from osgeo import gdal
import numpy as np
import pandas as pd
import os
import glob


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='str',
                        help='Directory that you want to scan for images')

    parser.add_argument('-sd',
                        '--scandate',
                        help='Scan date for images',
                        metavar='str',
                        type=str,
			required=True,
                        default=None)

    parser.add_argument('-o',
                        '--outdir',
                        help='Output filename',
                        metavar='str',
                        type=str,
                        default='img_coords_out/')

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Collect coordinates and make a CSV file"""

    args = get_args()
    # Make the ouput directory
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    # Scan for tif images in input directory
    images = glob.glob(args.dir + "*.tif", recursive=True)
    #print(images)
    loc_gps = {}
    file_list = []
    u_l_list = []
    l_l_list = []
    u_r_list = []
    l_r_list = []
    center_list = []

    for i in images:
        gps = []
        filename = os.path.basename(i)
        ds = gdal.Open(i)
        # print(filename)
        meta = gdal.Info(ds)
        coord_list = []
        lines = meta.splitlines()
        coord_sys = lines[17]
        # Split line to get only the coordiantes
        u_l = lines[35].split()[2:4]
        l_l = lines[36].split()[2:4]
        u_r = lines[37].split()[2:4]
        l_r = lines[38].split()[2:4]
        center = lines[39].split()[1:3]
        # Join the coordinates into a string
        u_l = ' '.join(u_l).strip('()')
        l_l = ' '.join(l_l).strip('()')
        u_r = ' '.join(u_r).strip('()')
        l_r = ' '.join(l_r).strip('()')
        center = ' '.join(center).strip('()')
        file_list.append(filename)
        u_l_list.append(u_l)
        l_l_list.append(l_l)
        u_r_list.append(u_r)
        l_r_list.append(l_r)
        center_list.append(center)

    d = {'Filename': file_list, 'Upper left': u_l_list, 'Lower left': l_l_list,
         'Upper right': u_r_list, 'Lower right': l_r_list, 'Center': center_list}
    df = pd.DataFrame(data=d)

    outfile = args.outdir + args.scandate + "_coordinates.csv"
    df.to_csv(outfile, index=False)

    print(f'Process complete, wrote coordinates in "{outfile}".')

# --------------------------------------------------
if __name__ == '__main__':
    main()
