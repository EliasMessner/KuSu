def main():
    data_dir = "data/"
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]     # the 3 files with the data
    count = 0                                                                                   # count the '\n' newline symbol

    for item in filepaths:                      # iterate through all files
        with open(data_dir + item, "r") as f:              # open the file in read-only
            count += f.read().count("\n")       # read the whole file, count the newlines, and immediate add it to the count
    print("{}".format(count))

if __name__ == "__main__":                      # for compatibility reasons if it is imported into other files
    main()
