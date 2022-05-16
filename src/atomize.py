import sys

def main():
    logs_dir = "../logs/"
    sourcepath = "../data/combined_data.xml"                    # where the entire XML data is now combined in one file

    with open(sourcepath, "r") as f:                    # read the whole source
        sourcedata = f.read()

    with open(logs_dir + "atomize.log", "w") as l:                 # set up a logging file
        l.write("File, Size, Lines\n")

    print("There are {} entries.".format(sourcedata.count("<lido:lido>")))      # a preview of how many output files there will be

    counter = 0                                                                 # counter each document
    posA = 0
    posB = 0
    while sourcedata.find("<lido:lido>", posB) != -1:                           # as long as there's another opening tag
        posA = sourcedata.find("<lido:lido>", posB)                             # start of opening tag
        posB = sourcedata.find("</lido:lido>", posA)+12                         # end of closing tag

        entrydata = sourcedata[posA:posB]                                       # the part to be put in its own file
        destinationPath = "../docs/atomized_{}.xml".format(counter)               # the file path to write it into

        with open(destinationPath, "w") as g:                                   # write this entry
            g.write(entrydata)

        with open(logs_dir + "atomize.log", "a") as l:
            logdata = "{}, {}, {}\n".format(counter, len(entrydata), entrydata.count("\n"))
            l.write(logdata)

        counter += 1
        sys.stdout.write("\r\tWrote {}".format(counter))


if __name__ == "__main__":
    main()
