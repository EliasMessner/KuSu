""" Please call this program from another python program as follows:

        import cleanResults
        cleanedData = cleanResults(results)

    results is the uncleaned output of the search engine as a string.
    cleanedData is returned as a string containing the JSON data.

    Alternatively you could comment out the return statement and instead write:

        with open("cleanedData.json", "w") as cdf:
            cdf.write(output)
"""


def main(data):
    cleanResults = []
    currentPos = 0
    while data.find("lido:lido", currentPos) != -1:         # as long as there are any more results
        cleanEntry = []

        currentPos = data.find("lido:lido", currentPos)                                 # gives the index of the first letter
        currentPos = data.find("lido:objectIdentificationWrap", currentPos+10)          # +11 to offset "'lido:lido'" and continue after it
        currentPos = data.find("'#text':", currentPos+30)                               # same principle
        startTitle = data.find("'", currentPos+8)+1                                     # the first letter of the actual title
        endTitle = data.find("'", startTitle)
        title = data[startTitle:endTitle]
        cleanEntry.append(f"'title':'{title}',\n")                                      # JSON as 'title':'foobar' pattern, to be combined later

        currentPos = data.find("lido:eventActor", currentPos)                           # can be extended by any tag with adjusted tags
        currentPos = data.find("lido:displayActorInRole", currentPos+16)                # must be in the same order as in the file though
        startActor = data.find("'", currentPos+25)+1
        endActor = data.find("'", startActor)
        actor = data[startActor:endActor]
        cleanEntry.append(f"'actor':'{actor}',\n")

        currentPos = data.find("lido:recordInfoSet", currentPos)
        currentPos = data.find("lido:recordInfoLink", currentPos+19)
        startURL = data.find("'", currentPos+20)+1
        endURL = data.find("'", startURL)
        URL = data[startURL:endURL]
        cleanEntry.append(f"'URL':'{URL}'\n")                                           # no final comma here to comply with valid JSON structure!

        cleanResults.append(cleanEntry)


    output = "{"                                                # generate the complete JSON file from scratch
    for i in range(len(cleanResults)):
        output += "'result" + str(i) + "':\n {"                 # {'result0':{...}, 'result1':{...}, 'result2':{...}}

        for item in cleanResults[i]:                            # equates to further 'key':'value' pairs being added within the { }
            output += "\t" + item

        if i == len(cleanResults)-1:                            # no comma separator after the last result
            output += "}\n"
        else:
            output += "},\n"                                    # add comma separator between results only
    output += "}"

    return output


if __name__ == "__main__":
        main()
