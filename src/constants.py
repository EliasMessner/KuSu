
import os


urls = ["https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_0.xml",
        "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_1.xml",
        "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_2.xml"]
muenchen_data_tar = "https://dmd.plus/opendata/digiporta/dm/dm_digiporta_xml-190221.tar.gz"

data_dir = str(os.path.join('..', 'data'))
logs_dir = str(os.path.join('..', 'logs'))
docs_dir = str(os.path.join('..', 'docs'))

image_filepaths = str(os.path.join("..", "images"))
images_westmuensterland = str(os.path.join("..", "images", "lamps"))

scale_percent = 5
n_clusters = 5
pbar_update_n = 1
plt_xticks_rotation = 'vertical'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

