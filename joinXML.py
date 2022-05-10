# EXPERIMENTAL FILE / DEPRECATED, use "combine.py" instead

def main():
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]             # the three files with the data
    destination = "mkg_lido-dC.web.xml"                                                                 # where to write it all

    data = []                                   # empty list for the contents of the three files

    for item in filepaths:                      # iterate through the files
        with open(item, "r") as f:              # open one read-only
            data.append(f.read())               # read the whole file and immediately append it to the list


    data = "\n\n".join(data)                # Merge all 3 file-contents into one, bad style though.
    with open(destination, "w") as f:       # open the target file
        f.write(data)

if __name__ == "__main__":                  # for compatibility reasons
    main()
