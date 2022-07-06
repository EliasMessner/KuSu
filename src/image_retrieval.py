from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)
import PIL
from scipy.spatial import KDTree
from scipy.stats import zipf

import extcolors
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np

import os

german_colors = {
    'Rot': ['Red', 'Tomato', 'Crimson', 'DarkRed', 'Firebrick', 'IndianRed', 'LightCoral', 'OrangeRed'],
    'Violett': ['Plum', 'Purple', 'RebeccaPurple', 'SlateBlue', 'Thistle', 'Violet', 'Orchid', 'MediumSlateBlue', 'MediumPurple', 'BlueViolet', 'DarkMagenta', 'DarkOrchid', 'DarkViolet', 'Indigo', 'Lavender', 'MediumOrchid'],
    'Blau': ['PowderBlue', 'RoyalBlue', 'SkyBlue', 'SteelBlue', 'Navy', 'MidnightBlue', 'MediumBlue', 'LightSkyBlue', 'AliceBlue', 'Aquamarine', 'Azure', 'Blue', 'CornflowerBlue', 'DarkBlue', 'DarkSlateBlue', 'DeepSkyBlue', 'DodgerBlue', 'LightBlue', 'LightCyan'],
    'Grün': ['PaleGreen', 'SeaGreen', 'SpringGreen', 'YellowGreen', 'Olive', 'OliveDrab', 'MediumSpringGreen', 'MediumSeaGreen', 'Lime', 'LimeGreen', 'LightGreen', 'Chartreuse', 'DarkGreen', 'DarkKhaki', 'DarkOliveGreen', 'DarkSeaGreen', 'ForestGreen', 'Green', 'GreenYellow', 'LawnGreen'],
    'Gelb': ['PaleGoldenRod', 'Yellow', 'Khaki', 'LemonChiffon', 'LightGoldenRodYellow'],
    'Orange': ['Coral', 'DarkOrange', 'DarkSalmon', 'LightSalmon', 'NavajoWhite', 'Orange'],
    'Schwarz': ['Black'],
    'Weiß': ['White'],
    'Grau': ['Snow', 'WhiteSmoke', 'SeaShell', 'Cornsilk', 'FloralWhite', 'GhostWhite', 'HoneyDew', 'Ivory', 'LightYellow', 'Linen', 'OldLace', 'PapayaWhip', 'Silver', 'SlateGrey', 'SlateGray', 'LightSteelBlue', 'DarkGrey', 'DarkGray', 'DarkSlateGrey', 'DarkSlateGray', 'LightSlateGrey', 'LightSlateGray', 'DimGrey', 'DimGray', 'Gainsboro', 'Grey', 'Gray', 'LightGray', 'LightGrey'],
    'Metallic': ['DarkGoldenRod', 'Gold', 'GoldenRod', 'Golden', 'Copper', 'Silver'],
    'Braun': ['PeachPuff', 'SandyBrown', 'Peru', 'SaddleBrown', 'Sienna', 'Tan', 'Wheat', 'AntiqueWhite', 'Beige', 'Bisque', 'BlanchedAlmond', 'Brown', 'BurlyWood', 'Chocolate', 'Maroon', 'Moccasin'],
    'Türkis-Blaugrün': ['PaleTurquoise', 'Teal', 'Turquoise', 'MintCream', 'Aqua', 'CadetBlue', 'Cyan', 'DarkCyan', 'DarkTurquoise', 'LightSeaGreen', 'MediumAquaMarine', 'MediumTurquoise'],
    'Pink-Rosa': ['PaleVioletRed', 'Pink', 'RosyBrown', 'Salmon', 'DeepPink', 'Fuchsia', 'Hotpink', 'LavenderBlush', 'LightPink', 'Magenta', 'MediumVioletRed', 'MistyRose']
}


def convert_rgb_to_names(rgb_tuple):
    colors = CSS3_HEX_TO_NAMES
    rgb_values = [hex_to_rgb(color) for color, color_name in colors.items()]
    rgb_values.append((142, 120, 81))
    rgb_values.append((92, 64, 50))
    rgb_values.append((153, 144, 139))

    names = [color_name for color, color_name in colors.items()]
    names.append('golden')
    names.append('copper')
    names.append('silver')

    kdt_db = KDTree(rgb_values, 200)
    distance, index = kdt_db.query(rgb_tuple)
    css_name = names[index]

    for value in german_colors.values():
        for color in value:
            index = list(german_colors.values()).index(value)
            if color.lower() == css_name:
                return list(german_colors.keys())[index]


def color_analysis_ext(image_path, file_path):
    colors, pixel_count = extcolors.extract_from_path(image_path, 8)
    colors = dict(colors)
    names = {}
    for (key, value) in colors.items():
        temp = (value / sum(colors.values())) * 100
        key_name = convert_rgb_to_names(key)
        if key_name in names:
            names[key_name] = names[key_name] + temp
        else:
            names[key_name] = temp
    names = {k: v for k, v in sorted(
        names.items(), key=lambda item: item[1], reverse=True)}
    file = open(file_path, "w+")
    for key, value in names.items():
        line = ""
        for i in range(1, int(value)):
            line += str(key) + ' '
        file.write(line + "\n")
    file.close()
    return names


def analyse_images(folder, file_folder):
    pbar = tqdm(total=len(os.listdir(folder)))
    color_dict_all = dict.fromkeys(german_colors.keys(), 0)
    for filename in os.listdir(folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
            continue
        img = PIL.Image.open(os.path.join(folder, filename))
        width, height = img.size
        new_size = (int(width/4), int(height/4))
        img = img.resize(new_size)
        result = color_analysis_ext(img, os.path.join(
            file_folder) + "/" + filename.split('.')[0] + ".txt")
        for (key, value) in color_dict_all.items():
            if key not in result.keys():
                continue
            color_dict_all[key] = value+result[key]
        pbar.update(n=1)
        result = {k: v for k, v in sorted(
            color_dict_all.items(), key=lambda item: item[1], reverse=True)}
        result = {k: v for k, v in result.items() if v >= 1}
    return result


def generate_plot(image_folder, file_folder, alpha, label, name):
    data = analyse_images(os.path.join(image_folder),
                          os.path.join(file_folder))
    total = sum(data.values())
    indices = range(len(data.values()))
    width = np.min(np.diff(indices)) / 3.
    fig, ax = plt.subplots()
    _ = ax.bar(indices + width / 2., data.values(), width)
    _ = ax.bar(indices - width / 2., [zipf.pmf(p, alpha) * total for p in range(1, len(data.values()) + 1)], width,
               color='black')
    _ = ax.set(xticks=indices, xticklabels=data.keys())
    _ = ax.set_xlabel(label)
    plt.savefig(name)


if __name__ == "__main__":
    import sys
    #color_analysis_ext(sys.argv[1], sys.argv[2])
    analyse_images(sys.argv[1], sys.argv[2])
