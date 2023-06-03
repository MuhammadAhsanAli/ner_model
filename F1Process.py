import pandas as pd
import sns as sns
import spacy
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from resources.lexicon import lexicon
import matplotlib.pyplot as plt

# Load the dataset from CSV
df = pd.read_csv('/home/ahsan/Documents/p/university/thesis/article_log/F1/fake.csv')

# Get the true labels from the DataFrame
true_labels = df['Entities']

# Perform the classification and obtain the predicted labels
# You need to replace this step with your actual classification code
nlp = spacy.load("custom_ner/output/model-best")
nlp.vocab["ٹوئٹر"].is_stop = True
nlp.vocab["ٹویٹر"].is_stop = True
texts = df['Text']

texts = texts.tolist()

print(texts)
ent_tag = []
for row in texts:
    abc = ''
    doc = nlp(row)
    # predict named entities and print the label and text for each entity
    for ent in doc.ents:
        if len(ent) > 0 and ent.text.lower() in lexicon:
            abc = ent.label_
    ent_tag.append(abc)

# else:
predicted_labels = ent_tag

# Calculate the confusion matrix
confusion_mat = confusion_matrix(true_labels, predicted_labels)

# Calculate precision, recall, and F1 score
precision = precision_score(true_labels, predicted_labels, average='weighted')
recall = recall_score(true_labels, predicted_labels, average='weighted')
f1 = f1_score(true_labels, predicted_labels, average='weighted')

# Print the results
print("Confusion Matrix:")
print(confusion_mat)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# Plot the confusion matrix as a heatmap
labels = ['Main', 'Reference']
sns.heatmap(confusion_mat, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Blues')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
sns.heatmap(confusion_mat, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Blues')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
