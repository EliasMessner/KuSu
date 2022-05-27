import requests
from constants import urls, data_dir


def download_xml_file(url, data_dir):
    r = requests.get(url, allow_redirects=True)
    file_name = url.split("/")[-1]
    open(data_dir + file_name, 'wb').write(r.content)


def get_data(data_dir):
    for url in urls:
        download_xml_file(url, data_dir)


if __name__ == "__main__":
    get_data(data_dir)
