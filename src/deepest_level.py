# This file finds the deepest level of the XML file
from src.constants import data_dir


def main():
    file_paths = ["mkg_lido-dC.web_0.xml", "mkg_lido-dC.web_1.xml", "mkg_lido-dC.web_2.xml"]     # the 3 files
    t_per_line = 0                                                                                # count variable the '\t'
    t_max = 0                                                                                    # maximal depth
    t_file = ""                                                                                  # which file it was in
    t_pos = 0                                                                                    # where in that file it was found

    for item in file_paths:                      # iterate through the whole list
        with open(data_dir + item, "r") as f:              # open the files in read-only
            data = f.read().split("\n")         # read the whole file and immediate split it by line
            for i in range(len(data)):              # go through each line in that file
                t_per_line = data[i].count("\t")      # count the tabs in that line
                if t_per_line >= t_max:                # if it's "deeper" than the previous record
                    t_max = t_per_line                 # update maximum depth
                    t_file = item                    # update the file where it was found
                    t_pos = i                        # update the line where it was found

    print("File {} at {}\nDepth {}".format(t_file, t_pos, t_max))      # output with the answer


if __name__ == "__main__":                      # for compatibility with other python scripts
    main()
