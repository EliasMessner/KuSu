# The XML data we get from our source is split in 3 files, each 58 - 73 MiB large.
# There are over 14.000 individual entries/documents in those files combined.
# We only perform searches on these huge strings, no editing of any kind. As editing
# a total of 197 MB of string each time we find an entry would consume enormous
# amounts of processing power on weak hardware. For that, each search on that string
# needs to be narrowed down. We search for closing tags only after the last opening tag,
# and we only search for opening tags after the last closing tag. Without this simple step it
# would only run at < 100 kiB/s, with it it processes the whole 197 MB in seconds.


import sys


def main():
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]         # files to be combined into one
    destination = "combined_data.xml"                                                               # destination

    for item in filepaths:                                          # go through each file
        with open(item, "r") as f:
            data = f.read()                                         # get complete content of each file

        filesize = round(len(data)/2**20, 3)                        # filesize in MiB
        print("Read {}\nSize: {} MB".format(item, filesize))

        processed = 0                                               # processed data in MiB
        posA = 0
        posB = 0
        with open(destination, "a") as g:
            while data.find("<lido:lido>", posB) != -1:             # keep appending as long as there's another opening tag
                posA = data.find("<lido:lido>", posB)               # find the opening tag, after the last closing tag
                posB = data.find("</lido:lido>", posA)+12           # find the end of the closing tag, search after the last opening tag

                entrydata = data[posA:posB]                         # the entry itself
                g.write(entrydata + "\n\n")                         # add that entry to the destination file

                processed += len(entrydata) / 2**20                                 # how much data is left in this file in MiB
                sys.stdout.write("\r\t{} MB done.".format(round(processed,3)))      # overwrite in the same line to avoid flooding the terminal
            print("\nFile done.\n")

if __name__ == "__main__":
    main()
