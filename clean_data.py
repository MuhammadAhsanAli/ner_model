import pandas as pd
from resource1 import dictionary
import re
######
# Clean the dataset and create spacy format json
######
# Read the Excel file
df = pd.read_csv('/home/ahsan/Documents/p/university/thesis/article_log/eng_article_log.csv')
total = 0
data = []
# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    # Extract the values from each column
    column1_value = row['Twitter']
    column2_value = row['Facebook']
    column3_value = row['Instagram']
    title = row['Title']
    if column1_value == 1 or column2_value == 1 or column3_value == 1:
        # Do something with the values
        total += 1
        rf = []
        for term in dictionary['term']:
            # Find the starting index of the keyword in the sentence

            start_index = re.sub('[^a-z0-9.]+', ' ', title.lower()).find(term)
            # If the keyword is found, calculate the ending index
            if start_index >= 0:
                end_index = start_index + len(term)
                rf.append([start_index, end_index, "MAIN"])
        data.append([re.sub('[^a-z0-9.]+', ' ', title.lower()), {"entities": rf}])
        #print(f"Row {total}: {column1_value}, {column2_value}, {column3_value}")

print(data)
print(total)