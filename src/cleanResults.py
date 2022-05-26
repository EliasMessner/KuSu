"""
Please use get_clean_results, as it handles multiple actors and titles
"""


def get_clean_results(response):
    """
    Returns a simplified, cleaned dict with user-readable info.
    :param response: the raw response from elasticsearch query
    :return: a user readable dict with important descriptive data for each hit
    """
    pretty_responses = []
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        pretty_response = {}

        title_set = source['lido:lido']['lido:descriptiveMetadata']['lido:objectIdentificationWrap']['lido:titleWrap']['lido:titleSet']
        title_set = title_set if isinstance(title_set, list) else [title_set]
        titles = [entry['lido:appellationValue']['#text'] for entry in title_set]

        events = source['lido:lido']['lido:descriptiveMetadata']['lido:eventWrap']['lido:eventSet']
        events = events if isinstance(events, list) else [events]
        actors = [event['lido:event']['lido:eventActor']['lido:displayActorInRole'] for event in events if event['lido:event'].get('lido:eventActor') is not None]

        url = source['lido:lido']['lido:administrativeMetadata']['lido:recordWrap']['lido:recordInfoSet']['lido:recordInfoLink']

        pretty_response["title(s)"] = titles[0] if len(titles) == 1 else titles
        pretty_response["actor(s)"] = actors[0] if len(actors) == 1 else actors
        pretty_response["url"] = url
        pretty_responses.append(pretty_response)
    return pretty_responses


def getCleanResults(data):
    """
    deprecated, use get_clean_results
    """
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


