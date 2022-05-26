import requests


def download_xml_file(url, data_dir):
    r = requests.get(url, allow_redirects=True)
    file_name = url.split("/")[-1]
    open(data_dir + "/" + file_name, 'wb').write(r.content)


def get_data(data_dir):
    urls = ["https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_0.xml",
            "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_1.xml",
            "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_2.xml"]
    for url in urls:
        download_xml_file(url, data_dir)


if __name__ == "__main__":
    get_data("../data")
