import sys

def main():
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]         # files to be combined into one
    destination = "combined_data.xml"                                                               # destination

    for item in filepaths:                                  # go through each file
        with open(item, "r") as f:
            data = f.read()                                 # get complete content of each file
            print("Read {}".format(item))

        with open(destination, "a") as g:                   # append to the destination file
            while data.find("<lido:lido>") != -1:           # go on as long as there's another entry to be added
                posA = data.find("<lido:lido>")             # find the start of the opening tag of 1 entry
                posB = data.find("</lido:lido>")+12         # find the end of the closing tag of that entry
                g.write(data[posA:posB] + "\n\n")           # add that entry to the destination file
                data = data[posB:]                          # remove that entry from the data
                remaining = round(len(data) / 2**20, 3)                         # how much data is left in this file in MB
                sys.stdout.write("\r{} MB remaining.".format(remaining))        # overwrite in the same line to avoid flooding the terminal
        print("\nWrote that part.")

if __name__ == "__main__":
    main()
