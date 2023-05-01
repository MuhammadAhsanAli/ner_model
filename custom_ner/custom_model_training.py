from spacy.training import docs_to_json, Example
import spacy
import random


# TRAIN_DATA = [
#     ("Instagram enabled new feature",
#      {"entities": [(0, 9, "MAIN")]}),
#     ("Whatsapp allowed multiple messages at once",
#      {"entities": [(0, 8, "MAIN")]})
# ]
TRAIN_DATA = [
    ("ایلون مسک نے ٹویٹر پر اشتہارات کے لئے ایپل سے جنگ چھیڑ دی",
     {"entities": [(13, 18, "MAIN")]}),
    ("فیس بک کی مالک کمپنی میٹا سے 11000 ملازمین فارغ",
     {"entities": [(0, 6, "MAIN")]})
]
nlp_def = spacy.blank("en")

# Define the new label scheme
LABELS = ["Main", "Reference"]
nlp = spacy.load("./output/model-best")

print(spacy.training.offsets_to_biluo_tags(nlp.make_doc("ایلون مسک نے ٹویٹر پر اشتہارات کے لئے ایپل سے جنگ چھیڑ دی"), [(39, 44, "MAIN")]))

#ner.add_label("MAIN")
#ner.add_label("REFERENCE")

#nlp = spacy.blank("en")

# the DocBin will store the example documents
ner = nlp.get_pipe("ner")


#for label in LABELS:
#    print(label)
 #   ner.add_label(label)

examples = []
nlp.begin_training()

#for text, annotations in TRAIN_DATA:
  #  print(annotations)
 #   examples.append(Example.from_dict(nlp.make_doc(text), annotations))

#nlp.update(examples)

# Train the model
optimizer = nlp.initialize()
for i in range(10):
    random.shuffle(TRAIN_DATA)
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], sgd=optimizer)

nlp.to_disk("./output/model-best")


