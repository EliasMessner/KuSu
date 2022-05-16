# This file finds the deepest level of the XML file

def main():
    data_dir = "data/"
    filepaths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]     # the 3 files
    tPerLine = 0                                                                                # count variable the '\t'
    tMax = 0                                                                                    # maximal depth
    tFile = ""                                                                                  # which file it was in
    tPos = 0                                                                                    # where in that file it was found

    for item in filepaths:                      # iterate through the whole list
        with open(data_dir + item, "r") as f:              # open the files in read-only
            data = f.read().split("\n")         # read the whole file and immediate split it by line
            for i in range(len(data)):              # go through each line in that file
                tPerLine = data[i].count("\t")      # count the tabs in that line
                if tPerLine >= tMax:                # if it's "deeper" than the previous record
                    tMax = tPerLine                 # update maximum depth
                    tFile = item                    # update the file where it was found
                    tPos = i                        # update the line where it was found

    print("File {} at {}\nDepth {}".format(tFile, tPos, tMax))      # output with the answer

if __name__ == "__main__":                      # for compatibility with other python scripts
    main()
