import copy
import tarfile

import requests, os, re
from constants import urls, data_dir, docs_dir, muenchen_data_tar
from pathlib import Path
from tqdm import tqdm


def download_file(url, data_dir):
    r = requests.get(url, allow_redirects=True)
    file_name = url.split("/")[-1]
    Path(data_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    open(os.path.join(data_dir, file_name), 'wb').write(r.content)


def extract_to(filename: str, dest_path: str):
    if filename.endswith("tar.gz"):
        tar = tarfile.open(filename, "r:gz")
    elif filename.endswith("tar"):
        tar = tarfile.open(filename, "r:")
    else:
        raise ValueError(f"Unsupported File Ending '{filename.split('.')[-1]}'")
    for member in tqdm(iterable=tar.getmembers(), total=len(tar.getmembers())):
        if member.isreg():  # skip if the TarInfo is not files
            member.name = os.path.basename(member.name)  # remove the path by reset it
            tar.extract(member=member, path=dest_path)
    tar.close()


def get_data(data_dir):
    print("Downloading MKG Data...")
    for url in tqdm(urls):
        download_file(url, data_dir)
    # muenchen data
    print("Downloading Muenchen Data...")
    download_file(muenchen_data_tar, data_dir)
    print("Done.")
    print("Extracting Muenchen Data...")
    filename = muenchen_data_tar.split('/')[-1]
    extract_to(os.path.join(data_dir, filename), docs_dir)


if __name__ == "__main__":
    get_data(data_dir)
