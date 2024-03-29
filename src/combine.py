# The XML data we get from our source is split in 3 files, each 58 - 73 MiB large.
# There are over 14.000 individual entries/documents in those files combined.
# We only perform searches on these huge strings, no editing of any kind. As editing
# a total of 197 MB of string each time we find an entry would consume enormous
# amounts of processing power on weak hardware. For that, each search on that string
# needs to be narrowed down. We search for closing tags only after the last opening tag,
# and we only search for opening tags after the last closing tag. Without this simple step it
# would only run at < 100 kiB/s, with it it processes the whole 197 MB in seconds.


import os
from pathlib import Path

from constants import data_dir


def combine(file_paths, dest_name):
    """
    :param file_paths: files to be combined into one
    :param dest_name: reference name for destination file
    """
    destination = os.path.join(data_dir, f'combined_data_{dest_name}.xml')
    # remove file if it exists (so we can create a new file from scratch)
    if os.path.exists(destination):
        os.remove(destination)
    # create the directory if not exists
    Path(data_dir).mkdir(parents=True, exist_ok=True)

    for item in file_paths:                                          # go through each file
        with open(os.path.join(data_dir, item), "r") as f:
            data = f.read()                                         # get complete content of each file

        file_size = round(len(data)/2**20, 3)                        # filesize in MiB
        # print("Read {}\nSize: {} MB".format(item, file_size))

        processed = 0                                               # processed data in MiB
        pos_a = 0
        pos_b = 0
        with open(destination, "a") as g:
            while data.find("<lido:lido>", pos_b) != -1:             # keep appending as long as there's another opening tag
                pos_a = data.find("<lido:lido>", pos_b)               # find the opening tag, after the last closing tag
                pos_b = data.find("</lido:lido>", pos_a)+12           # find the end of the closing tag, search after the last opening tag

                entry_data = data[pos_a:pos_b]                         # the entry itself
                g.write(entry_data + "\n\n")                         # add that entry to the destination file

                processed += len(entry_data) / 2**20                                 # how much data is left in this file in MiB
                # sys.stdout.write("\r\t{} MB done.".format(round(processed,3)))      # overwrite in the same line to avoid flooding the terminal
            # print("\nFile done.\n")
