
def parse_lido_entry(lido_entry):
    result = {}

    _id = lido_entry['lido:lido']['lido:lidoRecID']['#text']
    result["id"] = _id

    titles = _parse_titles(lido_entry)
    result["titles"] = titles

    category = lido_entry['lido:lido']['lido:category']['lido:conceptID']['#text']
    result["category"] = category

    classification_terms = _parse_classification_terms(lido_entry)
    result["classification"] = classification_terms

    work_type = _parse_work_type(lido_entry)
    result["work_type"] = work_type

    inscriptions = _parse_inscriptions(lido_entry)
    result["inscriptions"] = inscriptions

    measurements = _parse_measurements(lido_entry)
    result["measurements"] = measurements

    events = _parse_events(lido_entry)
    result["events"] = events

    related_subjects = _parse_related_subjects(lido_entry)
    result["related_subjects"] = related_subjects

    # related work, possible todo
    # ['lido:lido']['lido:descriptiveMetadata']['lido:objectRelationWrap']['lido:relatedWorksWrap']['lido:relatedWorkSet']['lido:relatedWorkRelType']['lido:term']['#text']
    # ['lido:lido']['lido:descriptiveMetadata']['lido:objectRelationWrap']['lido:relatedWorksWrap']['lido:relatedWorkSet']

    url = lido_entry['lido:lido']['lido:administrativeMetadata']['lido:recordWrap']['lido:recordInfoSet'][
        'lido:recordInfoLink']
    result["url"] = url

    work_id = lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectIdentificationWrap']['lido:repositoryWrap']['lido:repositorySet']['lido:workID']['#text']
    result["work_id"] = work_id

    return result


def _parse_related_subjects(lido_entry):
    subject_set = (lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectRelationWrap'].get('lido:subjectWrap') or {}).get('lido:subjectSet', [])
    subject_set = subject_set if isinstance(subject_set, list) else [subject_set]
    related_subjects = []
    for subject in subject_set:
        if subject['lido:subject'].get('lido:subjectConcept') is not None:
            term_set = subject['lido:subject']['lido:subjectConcept']['lido:term']
            term_set = term_set if isinstance(term_set, list) else [term_set]
            related_subjects += [t['#text'] for t in term_set if t.get('#text') is not None]
        if subject['lido:subject'].get('lido:subjectActor') is not None:
            name_actor_set = subject['lido:subject']['lido:subjectActor']['lido:actor']['lido:nameActorSet']
            name_actor_set = name_actor_set if isinstance(name_actor_set, list) else [name_actor_set]
            related_subjects += [name_actor['lido:appellationValue'].get('#text', "") for name_actor in name_actor_set]
    return related_subjects


def _parse_events(lido_entry):
    events = lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:eventWrap']['lido:eventSet']
    events = events if isinstance(events, list) else [events]
    resulting_events = []
    for event in events:
        event_type = event['lido:event']['lido:eventType']['lido:term']['#text']
        event_actors = event['lido:event'].get('lido:eventActor')
        if event_actors is None:
            event_actors = []
        elif not isinstance(event_actors, list):
            event_actors = [event_actors]
        actors = [event_actor['lido:displayActorInRole']
                  for event in events
                  for event_actor in event_actors]
        earliest_date = (event['lido:event'].get('lido:eventDate', {}).get('lido:date') or {}).get('lido:earliestDate', "")
        latest_date = (event['lido:event'].get('lido:eventDate', {}).get('lido:date') or {}).get('lido:latestDate', "")
        materials_tech_list = event['lido:event'].get('lido:eventMaterialsTech')
        if materials_tech_list is None:
            materials_tech_list = []
        elif not isinstance(materials_tech_list, list):
            materials_tech_list = [materials_tech_list]
        materials = [mt['lido:displayMaterialsTech'] for mt in materials_tech_list]
        resulting_events.append({"type": event_type,
                                 "actors": actors,
                                 "date": [earliest_date, latest_date],
                                 "materials": materials})
    return resulting_events


def _parse_measurements(lido_entry):
    measurements = (lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectIdentificationWrap'].get('lido:objectMeasurementsWrap') or {}).get('lido:objectMeasurementsSet', {}).get('lido:displayObjectMeasurements', "")
    return measurements


def _parse_inscriptions(lido_entry):
    inscriptions_list = lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectIdentificationWrap']['lido:inscriptionsWrap'][
        'lido:inscriptions']
    inscriptions_list = inscriptions_list if isinstance(inscriptions_list, list) else [inscriptions_list]
    inscriptions = [inscription['lido:inscriptionDescription']['lido:descriptiveNoteValue'] for inscription in
                    inscriptions_list]
    return inscriptions


def _parse_work_type(lido_entry):
    work_type_terms = lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectClassificationWrap']['lido:objectWorkTypeWrap'][
        'lido:objectWorkType'].get('lido:term')
    if work_type_terms is not None:
        work_type_terms = work_type_terms if isinstance(work_type_terms, list) else [work_type_terms]
        work_type = [dt.get('#text', "") for dt in work_type_terms]
    else:
        work_type = ""
    return work_type


def _parse_classification_terms(lido_entry):
    classification_list = lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectClassificationWrap'].get(
        'lido:classificationWrap', {}).get('lido:classification', [])
    classification_list = classification_list if isinstance(classification_list, list) else [classification_list]
    classification_terms = []
    for c in classification_list:
        term_list = c['lido:term']
        term_list = term_list if isinstance(term_list, list) else [term_list]
        classification_terms += [t.get('#text', "") for t in term_list]
    return classification_terms


def _parse_titles(lido_entry):
    title_set = lido_entry['lido:lido']['lido:descriptiveMetadata']['lido:objectIdentificationWrap']['lido:titleWrap'][
        'lido:titleSet']
    title_set = title_set if isinstance(title_set, list) else [title_set]
    titles = [entry['lido:appellationValue']['#text'] for entry in title_set]
    return titles
