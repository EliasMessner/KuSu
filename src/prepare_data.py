"""
Script for downloading and preparing all the data for indexing
"""

from get_data import get_data
from combine import combine
from atomize import atomize_all
from constants import data_dir


if __name__ == "__main__":
    get_data(data_dir)
    file_paths_mkg = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]
    file_paths_westmuensterland = ["LIDO_Exp.XML"]
    combine(file_paths_mkg, "mkg")
    combine(file_paths_westmuensterland, "westmuensterland")
    atomize_all()
