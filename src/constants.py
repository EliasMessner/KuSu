
import os


urls = ["https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_0.xml",
        "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_1.xml",
        "https://raw.githubusercontent.com/MKGHamburg/MKGCollectionOnlineLIDO_XML/master/mkg_lido-dC.web_2.xml"]
muenchen_data_tar = "https://dmd.plus/opendata/digiporta/dm/dm_digiporta_xml-190221.tar.gz"

data_dir = str(os.path.join('..', 'data'))
logs_dir = str(os.path.join('..', 'logs'))
docs_dir = str(os.path.join('..', 'docs'))

images_muenchen = str(os.path.join("..", "images", "muenchen"))
images_westmuensterland = str(os.path.join("..", "images", "westmuensterland"))

textfiles_muenchen = str(os.path.join("..", "images", "muenchentext"))
textfiles_westmuensterland = str(os.path.join("..", "images", "westmuensterlandtext"))

scale_percent = 5
n_clusters = 5
pbar_update_n = 1
plt_xticks_rotation = 'vertical'


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


def get_settings(boost: dict[str, float], similarity: str, analyzer: str) -> dict:
    """
    Constructs a dict for elasticsearch settings.
    """
    assert analyzer in ["german_analyzer", "german_light_analyzer"]
    return {
        "settings": {
            "analysis": {

                "filter": {
                    "german_stop": {
                        "type": "stop",
                        "stopwords": "_german_"
                    },
                    "german_stemmer": {
                        "type": "stemmer",
                        "language": "german"
                    },
                    "german_light_stemmer": {
                        "type": "stemmer",
                        "language": "light_german"
                    }
                    # TODO maybe also use german2, minimal_german stemmers https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stemmer-tokenfilter.html
                },

                "analyzer": {
                    "german_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "german_stop",
                            "german_normalization",
                            "german_stemmer"
                        ]
                    },
                    "german_light_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "german_stop",
                            "german_normalization",
                            "german_light_stemmer"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    #"type": "text",
                    "enabled": False,
                },
                "img_id": {
                    "enabled": False
                },
                "titles": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("titles", 1),
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "classification": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("classification", 1)
                },
                "work_type": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("work_type", 1)
                },
                "inscriptions": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("inscriptions", 1)
                },
                "measurements": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("measurements", 1)
                },
                "events": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("events", 1)
                },
                "related_subjects": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("related_subjects", 1)
                },
                "colors": {
                    "type": "text",
                    "similarity": similarity,
                    "analyzer": analyzer,
                    "boost": boost.get("colors", 1)
                },
                "url": {
                    #"type": "text",
                    "enabled": False
                },
                "img_url": {
                    #"type": "text",
                    "enabled": False
                }
            }
        }
    }


boost_default = {}  # all values 1
boost_2 = {
    "titles": 2,
    "related_subjects": 0.5
}
