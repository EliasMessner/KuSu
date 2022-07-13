import re
from collections.abc import Iterable
import validators


def parse_lido_entry(lido_entry, filename):
    """
    Parses a lido entry to a dictionary only containing information relevant for retrieval.
    :param filename: name of the xml file in docs folder
    :param lido_entry: the lido entry as dict
    :return: a dict ready for retrieval process
    """
    result = {}
    result["filename"] = filename
    result["id"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:lidoRecID'], is_text=True, default="")
    result["img_id"] = parse_img_id(lido_entry)
    result["titles"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectIdentificationWrap', 'lido:titleWrap', 'lido:titleSet', 'lido:appellationValue'], is_text=True, default="")
    result["classification"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectClassificationWrap', 'lido:classificationWrap', 'lido:classification', 'lido:term'], is_text=True, default="")
    result["work_type"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectClassificationWrap', 'lido:objectWorkTypeWrap', 'lido:objectWorkType', 'lido:term'], is_text=True, default="")
    result["inscriptions"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectIdentificationWrap', 'lido:inscriptionsWrap', 'lido:inscriptions', 'lido:inscriptionDescription', 'lido:descriptiveNoteValue'], is_text=False, default="")
    description = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectIdentificationWrap', 'lido:objectDescriptionWrap', 'lido:objectDescriptionSet', 'lido:descriptiveNoteValue'], is_text=True, default="")
    description = description[0] if isinstance(description, list) and len(description) else description
    result["inscriptions"] += "\n" + description
    result["measurements"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectIdentificationWrap', 'lido:objectMeasurementsWrap', 'lido:objectMeasurementsSet', 'lido:displayObjectMeasurements'], is_text=True, default="")
    result["events"] = parse_events(lido_entry)
    result["related_subjects"] = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectRelationWrap', 'lido:subjectWrap', 'lido:subjectSet', 'lido:subject', 'lido:subjectConcept', 'lido:term'], is_text=True, default="")
    result["url"] = parse_url(lido_entry)
    result["img_url"] = parse_img_url(lido_entry)
    # remove urls
    result["classification"] = remove_urls(result["classification"])
    result["related_subjects"] = remove_urls(result["related_subjects"])
    result["work_type"] = remove_urls(result["work_type"])
    all_values_to_string(result)
    return result


def remove_urls(iterable: list[str]):
    return [element for element in iterable if not validators.url(element)]


def all_values_to_string(result):
    for key, value in result.items():
        if key in ["events", "img_url", "img_id", "colors", "filename"] or isinstance(value, str):
            continue
        assert isinstance(value, Iterable)
        result[key] = ', '.join(flatten(value))
        result[key] = re.sub(r"\s+", " ", result[key])
    event_strings = []
    for event in result["events"]:
        event_string = ""
        if event.get("types") is not None:
            event_string += ', '.join(flatten(event["types"]))
        if event.get("actors") is not None:
            if event_string != "":
                event_string += ': '
            event_string += ', '.join(flatten(event["actors"]))
        if event.get("date") is not None:
            if event_string != "":
                event_string += ' '
            event_string += '(' + event["date"][0]
            if "" not in event["date"]:
                event_string += " - "
            event_string += event["date"][1] + ')'
        if event.get("materials") is not None:
            if event_string != "":
                event_string += '; '
            event_string += ', '.join(flatten(event["materials"]))
        event_strings.append(event_string)
    result["events"] = "\n".join(event_strings)


def parse_img_id(lido_entry):
    """
    The img_id will be used as the filename for image retrieval
    """
    # img id for muenchen comes from resourceID
    img_id = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:administrativeMetadata', 'lido:resourceWrap', 'lido:resourceSet', 'lido:resourceID'], is_text=True, default=[None])
    if len(img_id) > 0:
        img_id = img_id[0]
        if img_id is not None and img_id.startswith("PT_"):
            return img_id
    # img id for westmuensterland comes from workID
    img_id = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:objectIdentificationWrap', 'lido:repositoryWrap', 'lido:repositorySet', 'lido:workID'], is_text=True, default=[None])
    if len(img_id) > 0:
        img_id = img_id[0]
        if img_id is not None and img_id.startswith("HM-"):
            return img_id
    return ""


def parse_events(lido_entry):
    event_data = find_values_by_key_list(lido_entry, ['lido:lido', 'lido:descriptiveMetadata', 'lido:eventWrap', 'lido:eventSet'], is_text=False, default=[])
    event_data = event_data if isinstance(event_data, list) else [event_data]
    resulting_events = []
    for event in event_data:
        new_event = {}
        event_types = find_values_by_key_list(event, ['lido:event', 'lido:eventType', 'lido:term'], is_text=True, default=[])
        if len(event_types) > 0:
            new_event["types"] = event_types
        event_actors = find_values_by_key_list(event, ['lido:event', 'lido:eventActor'], is_text=True, default=[])
        if len(event_actors) > 0:
            new_event["actors"] = event_actors
        earliest_date = find_values_by_key_list(event, ['lido:event', 'lido:eventDate', 'lido:date', 'lido:earliestDate'], is_text=True, default="")
        latest_date = find_values_by_key_list(event, ['lido:event', 'lido:eventDate', 'lido:date', 'lido:latestDate'], is_text=True, default="")
        earliest_date = earliest_date[0] if len(earliest_date) else ""
        latest_date = latest_date[0] if len(latest_date) else ""
        if earliest_date != "" or latest_date != "":
            new_event["date"] = [earliest_date, latest_date]
        materials = find_values_by_key_list(event, ['lido:event', 'lido:eventMaterialsTech', 'lido:displayMaterialsTech'], is_text=False, default="")
        if len(materials) > 0:
            new_event["materials"] = materials
        if len(new_event) > 0:
            resulting_events.append(new_event)
    return resulting_events


def parse_img_url(lido_entry):
    img_urls = find_values_by_key_list(lido_entry,
                             ['lido:lido', 'lido:administrativeMetadata', 'lido:resourceWrap', 'lido:resourceSet',
                              'lido:resourceRepresentation', 'lido:linkResource'], is_text=True, default=[''])
    img_urls = img_urls if isinstance(img_urls, list) else [img_urls]
    # we use the first element found, because on our data the same link is present several times for each lido.
    # Appending '' to the retrieved list, because if an empty list is returned we need to avoid index error
    return (img_urls + [''])[0]


def parse_url(lido_entry):
    possible_urls = find_values_by_key_list(lido_entry,
                            ['lido:lido', 'lido:administrativeMetadata', 'lido:recordWrap', 'lido:recordInfoSet'],
                            is_text=True, default="")
    # remove all non-urls
    return [element for element in possible_urls if validators.url(element)]


def find_values_by_key_list(d: dict | list, keys: list, is_text: bool, default: any, result=None):
    """
    Searches dict for keys in given order, returns a list of all found values. If any key is not present,
    return default value. If is_text=True, performs nested search for '#text' at the end.
    :param d: the dict to search on
    :param keys: the keys in correct order
    :param is_text: If set to true, the last key in the key list is assumed to be "#text". No other key may be "#text"
    :param default: default value to return if any of the keys is not present
    :param result: only used for recursive calls. Do not set this parameter for an initial call
    :return: List of all found values, as strings.
    """
    if result is None:
        result = []
    if isinstance(d, list):
        for item in d:
            find_values_by_key_list(d=item, keys=keys, is_text=is_text, default=default, result=result)
    elif isinstance(d, dict):
        key = keys[0]
        if key == "#text":
            raise ValueError("Key '#text' not allowed. If you are searching for the #text key as last key, "
                             "set is_text to True.")
        value = d.get(key)
        if isinstance(value, str):
            result.append(value)
            return result
        if value is None:
            return default
        if len(keys) == 1:
            value = value if isinstance(value, list) else [value]
            for item in value:
                if is_text:
                    result += find_text_values(item, default)
                else:
                    result.append(item)
        else:
            find_values_by_key_list(d=value, keys=keys[1:], is_text=is_text, default=default, result=result)
    if len(result) == 0:
        return default
    if is_text and isinstance(result, list):
        # remove duplicates
        result = list(set(result))
    return flatten(result) if is_text else result


def find_text_values(d: dict, default: any):
    """
    Searches for values associated with the key '#text', and returns them as a list. If a key beginning with
    'lido:display' is present, only the sub-dict associated with that key will be searched. That's because the text
    values we are looking for (natural language) are sometimes present in a lido:display sub-dict, while other #text
    values outside that sub-dict are not natural language
    :param d: the dict to be searched
    :param default: default value to return if no #text keys were found
    """
    # search for lido:display key
    display_values = find_values_by_key_condition(d, lambda key: key.startswith("lido:display"))
    if len(display_values) > 1:
        raise ValueError("Multiple 'lido:display' keys are present. Please specify more keys.")
    elif len(display_values) == 1:
        # exactly one lido:display key was found, search for #text keys only in the display sub-dict
        text_values = find_values_by_key_condition(display_values[0], lambda key: key == "#text")
    else:
        # no lido:display key was found, search for raw #text key
        text_values = find_values_by_key_condition(d, lambda key: key == "#text")
    if len(text_values) == 0:
        return default
    return flatten(list(set(text_values)))


def find_values_by_key_condition(d: dict | list, condition: callable(str), result=None):
    """
    Searches given dict for keys that fulfill a condition. The values associated with those keys are returned as a list
    :param d: the dict to be searched
    :param condition: condition that a key must fulfill, can be a lambda expression or any callable
    :param result: only used for recursive calls. Do not set this parameter for an initial call
    :return: list of values associated with matching keys, or default value if none were found
    """
    if result is None:
        result = []
    if isinstance(d, dict):
        for key, value in d.items():
            if condition(key):
                result.append(value)
                return result
            find_values_by_key_condition(value, condition, result)
    elif isinstance(d, list):
        for item in d:
            find_values_by_key_condition(item, condition, result)
    return flatten(result)


def flatten(iterable: Iterable):
    return list(flatten_helper(iterable))


def flatten_helper(iterable: Iterable):
    for x in iterable:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten_helper(x)
        else:
            yield x


def prettify_authors(hit) -> str:
    authors = []
    for event in hit['_source']['events']:
        author = ""
        if event.get('actors') is None:
            continue
        author += event['actors']
        if event.get('actors') is not None:
            author += f" ({event['types']})"
        authors.append(author)
    authors = '; '.join(authors)
    return authors


def prettify(hit, include_title=True):
    """
    Returns a human-readable german string from a hit as returned by Elasticsearch.
    :param hit: the hit from the ES response, can be found under res['hits’]['hits'].
    :param include_title: True if the title should be included in the string.
    """
    result = f"Titel: {hit['_source']['titles']}\n" if include_title else ""
    result += f"Beschreibung: {hit['_source']['inscriptions']}\n" \
              f"Klassifikation: {hit['_source']['classification']}\n" \
              f"Kategorie: {hit['_source']['work_type']}\n" \
              f"Maße: {hit['_source']['measurements']}\n" \
              f"Ereignisse: {hit['_source']['events']}\n" \
              f"Verwandte Themen: {hit['_source']['related_subjects']}\n" \
              f"Bild-URL: {hit['_source']['img_url']}\n"
    return result


def get_title_and_img_string(hit):
    result = f"Titel: {hit['_source']['titles']}\n" \
             f"Bild-URL: {hit['_source']['img_url']}\n"
    return result
