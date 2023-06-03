import spacy
from spacy.tokens import DocBin
import json
import langid

######
# Create .spacy format file from json
######

# Open the file in read mode
with open('./data/mix_train_data_updated.jsonl', 'r') as f:
    # Load the JSON data from the file
    data = json.load(f)

nlp = spacy.blank("en")
nlp1 = spacy.blank("ur")
nlp1.vocab["ٹوئٹر"].is_stop = True

# the DocBin will store the example documents
db = DocBin()
for text, annotations in data:
    lang, score = langid.classify(text)
    print(text)
    doc = nlp(text)
    if lang != "en":
        doc = nlp1(text)

    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./train.spacy")