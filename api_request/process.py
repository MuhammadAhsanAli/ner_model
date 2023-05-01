import sys

sys.path.append('../')
import json
import spacy
from classification_lib import is_urdu_or_english
from resources.lexicon import lexicon
######
# Process incoming request and return response
######

def classify(data):
    global title
    data_dict = json.loads(data)
    sentences = data_dict['data']

    # load the custom model
    nlp = spacy.load(".././custom_ner/output/model-best")
    nlp.vocab["ٹوئٹر"].is_stop = True

    result = []
    for rows in sentences:
        for row in rows:
            title = row['title']
            # create a Doc object from the new sentence
            doc = nlp(title)
            ent_tag = []
            # predict named entities and print the label and text for each entity
            for ent in doc.ents:
                if len(ent) > 0 and ent.text.lower() in lexicon:
                    ent_tag.append([ent.text, ent.label_, lexicon[ent.text.lower()]])
            # else:
            # can add manual logic to handle it
            # ent_tag.append([ent.text, ent.label_, lexicon[]])

            result.append([title, ent_tag, is_urdu_or_english(title), row['created_at']])
    return result
