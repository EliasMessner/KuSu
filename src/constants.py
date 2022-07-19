import os

urls = ["https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_0.xml",
        "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_1.xml",
        "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_2.xml"]
muenchen_data_tar = "https://dmd.plus/opendata/digiporta/dm/dm_digiporta_xml-190221.tar.gz"

data_dir = str(os.path.join('..', 'data'))
logs_dir = str(os.path.join('..', 'logs'))
docs_dir = str(os.path.join('..', 'docs'))
queries_dir = str(os.path.join('..', 'queries'))
run_files_dir = str(os.path.join('..', 'run_files'))
qrels_dir = str(os.path.join('..', 'qrels'))
query_results_dir = str(os.path.join('..', 'query_results'))
plots_dir = str(os.path.join('..', 'plots'))

images_muenchen = str(os.path.join("..", "images", "muenchen"))
images_westmuensterland = str(os.path.join("..", "images", "westmuensterland"))

textfiles_muenchen = str(os.path.join("..", "images", "muenchentext"))
textfiles_westmuensterland = str(os.path.join("..", "images", "westmuensterlandtext"))

scale_percent = 5
n_clusters = 5
pbar_update_n = 1
plt_xticks_rotation = 'vertical'

default_index_name = 'boost_default-german_light_analyzer-boolean'

# query modes
only_disjunction = "only_disjunction"
combined_operators = "combined_operators"


class FontSizes:
    SMALL_SIZE = 8
    MEDIUM_SIZE = 10
    BIGGER_SIZE = 12


# font colors in terminal output
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
