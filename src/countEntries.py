def main():
    data_dir = "data/"
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]     # the 3 files with the original data
    count_open = 0                                                                              # count the opening <lido:lido> Tags
    count_close = 0                                                                             # count for closing </lido:lido> for control

    for item in filepaths:                                  # iterate through all 3 files
        with open(data_dir + item, "r") as f:                          # open one file
            data = f.read()                                 # read the whole file
            count_open += data.count("<lido:lido>")         # count how many opening tags there are and add it to the count
            count_close += data.count("</lido:lido>")

    print("{}\n{}".format(count_open, count_close))


if __name__ == "__main__":              # for compatibility should it be imported into other files
    main()
