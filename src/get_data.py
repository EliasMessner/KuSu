import requests
from constants import urls, data_dir
from pathlib import Path


def download_xml_file(url, data_dir):
    r = requests.get(url, allow_redirects=True)
    file_name = url.split("/")[-1]
    Path(data_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    open(data_dir + file_name, 'wb').write(r.content)


def get_data(data_dir):
    for url in urls:
        download_xml_file(url, data_dir)


if __name__ == "__main__":
    get_data(data_dir)
