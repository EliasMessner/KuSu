# Dependencies:
import extcolors
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import random
from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb)

def rgb_to_hex(rgb_color):
    # This code originally belongs to 
    # TO DO!
    hex_color = "#"
    for i in rgb_color:
        i = int(i)
        hex_color += ("{:02x}".format(i))
    return hex_color 

def convert_rgb_to_names(rgb_tuple):
    # This code originally belongs to 
    # TO DO!
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]

import extcolors
def color_analysis_ext(image_path, file_path):
    colors, pixel_count = extcolors.extract_from_path(image_path)
    colors = dict(colors)
    names = {convert_rgb_to_names(key): value/sum(colors.values()) for (key, value) in colors.items()}
    file = open(file_path, "w+")
    line = str([name for name in names.keys()])
    file.write(line)
    return names  

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()


