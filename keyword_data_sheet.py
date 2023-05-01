import pandas as pd
import re
import csv
######
# Select data row from sheet where any of keyword found
######

# Read the Excel file
df = pd.read_csv('/home/ahsan/Documents/p/university/thesis/article_log/urdu_article_log.csv', low_memory=False)
total = 0
data = []
path_to_file = ""
i = 0
# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    # Extract the values from each column
    column1_value = row['Twitter']
    column2_value = row['Facebook']
    column3_value = row['Instagram']
    title = row['Title']
    if column1_value == 1 or column2_value == 1 or column3_value == 1:
        i += 1
        data.append([i, row['Date'], title])


# Create a new CSV file
with open('/home/ahsan/Documents/p/university/thesis/article_log/urdu_keyword_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)

print('CSV file created successfully!')

print(data)
print(total)