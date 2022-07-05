"""
Script for downloading and preparing all the data for indexing
"""

from get_data import get_data
from combine import combine
from atomize import atomize
from constants import data_dir


if __name__ == "__main__":
    get_data(data_dir)
    combine()
    atomize()
