import re
import json
######
# Clean the dataset and create spacy format json
######
# Read the Excel file
total = 0
data = []

terms = ["انسٹا گرام", "انسٹاگرام", "ٹوئٹر", "ٹویٹر", "فیس بک", "فيس بک"];
#terms = ["instagram", "twitter", "facebook"];


# Load JSON data from a file
with open('custom_ner/data/ref_urdu_formatted.json', 'r') as f:
    data = json.load(f)
total = 0
result = []
for row in data:
    # Access the data within the row
    print(row[0])
    title = row[0]
    # Do something with the values
    total += 1
    rf = []
    te_count = 0
    for term in terms:
        te_count += 1
        # Find the starting index of the keyword in the sentence
        start_index = re.sub('[^؀-ۿ۞۩ؠ-ؿ0-9٠-٩\s]+', ' ', title.lower()).find(term)
        # If the keyword is found, calculate the ending index
        if start_index >= 0:
            end_index = start_index + len(term)
            rf.append([start_index, end_index, "REFERENCE"])
            result.append([re.sub('[^؀-ۿ۞۩ؠ-ؿ0-9٠-٩\s]+', ' ', title.lower()), {"entities": rf}])
        else:
            continue

print(result)
print(total)