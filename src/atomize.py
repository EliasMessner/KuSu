import sys, os
from pathlib import Path

from constants import logs_dir, docs_dir, data_dir


def atomize(source_file_name):
    """
    :param source_file_name: where the entire XML data is now combined in one file
    """
    Path(data_dir).mkdir(parents=True, exist_ok=True)  # create the directory if not exists
    Path(docs_dir).mkdir(parents=True, exist_ok=True)
    Path(logs_dir).mkdir(parents=True, exist_ok=True)
    source_path = os.path.join(data_dir, source_file_name)

    with open(source_path, "r") as f:                    # read the whole source
        source_data = f.read()

    with open(os.path.join(logs_dir, "atomize.log"), "w") as l:                 # set up a logging file
        l.write("File, Size, Lines\n")

    print("Atomizing {} entries.".format(source_data.count("<lido:lido>")))      # a preview of how many output files there will be

    counter = 0                                                                 # counter each document
    pos_a = 0
    pos_b = 0
    while source_data.find("<lido:lido>", pos_b) != -1:                           # as long as there's another opening tag
        pos_a = source_data.find("<lido:lido>", pos_b)                             # start of opening tag
        pos_b = source_data.find("</lido:lido>", pos_a)+12                         # end of closing tag

        entry_data = source_data[pos_a:pos_b]                                       # the part to be put in its own file
        data_source_ref = source_file_name.split('.')[0].split('_')[-1]
        destination_path = os.path.join(docs_dir, f"atomized_{data_source_ref}_{counter}.xml")          # the file path to write it into

        with open(destination_path, "w") as g:                                   # write this entry
            g.write(entry_data)

        with open(os.path.join(logs_dir, "atomize.log"), "a") as l:
            log_data = "{}, {}, {}\n".format(counter, len(entry_data), entry_data.count("\n"))
            l.write(log_data)

        counter += 1
        sys.stdout.write("\r\tDone atomizing {} entries.".format(counter))


def atomize_all():
    filenames = [filename for filename in os.listdir(data_dir) if filename.startswith("combined_data_") and filename.endswith(".xml")]
    for filename in filenames:
        atomize(filename)
