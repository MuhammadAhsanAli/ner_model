import json
import spacy
######
# Predict test data label by trained model
######
with open('./data/eng_testing.jsonl', 'r') as f:
    # Load the JSON data from the file
    data = json.load(f)

# load the custom model
nlp = spacy.load("./output/model-best")
#nlp.vocab["ٹوئٹر"].is_stop = True

total_correct = 0
total_incorrect = 0
correct = []
incorrect = []
for row in data:
    title = row[0]
    # create a Doc object from the new sentence
    doc = nlp(title)

    # predict named entities and print the label and text for each entity
    for label, ent in zip(row[1]['entities'], doc.ents):
        if title[label[0]:label[1]] == ent.text and label[2] == ent.label_:
            total_correct += 1
            correct.append([row[0], ent.text, ent.label_ ])
        else:
            total_incorrect += 1
            incorrect.append([title, ent.text, ent.label_ ])


print("Total Correct: "+str(total_correct))
print("Total Incorrect: "+str(total_incorrect))
print("Total: "+str(total_correct+total_incorrect))
print("correct array")
print(correct)
print("incorrect array")
print(incorrect)