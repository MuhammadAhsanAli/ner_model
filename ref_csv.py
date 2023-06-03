import csv
import json
from datetime import datetime, timedelta
import random

def generate_random_date():
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")


def extract_referenced_text(json_data):
    entities = json_data[1].get("entities", [])

    references = 0
    main = 0
    for entity in entities:
        if isinstance(entity, list) and len(entity) >= 3 and entity[2] == "REFERENCE":
            references += 1
        if isinstance(entity, list) and len(entity) >= 3 and entity[2] == "MAIN":
            main += 1

    if references == len(entities):
        return "REFERENCE"
    elif main == len(entities):
        return "MAIN"
    else:
        return "MIX"


def process_json_to_csv(json_file, csv_file):
    keywords = ["انسٹا گرام", "انسٹاگرام", "ٹوئٹر", "ٹویٹر", "فیس بک", "فيس بک"]

    with open(json_file, "r") as file:
        data = json.load(file)

    rows = []
    for item in data:
        title = item[0]
        date = generate_random_date()
        twitter = 1 if any(keyword in title.lower() and (keyword == "ٹویٹر" or keyword == "ٹوئٹر") for keyword in keywords) else 0
        instagram = 1 if any(keyword in title.lower() and (keyword == "انسٹا گرام" or keyword == "انسٹاگرام") for keyword in keywords) else 0
        facebook = 1 if any(keyword in title.lower() and (keyword == "فیس بک" or keyword == "فيس بک") for keyword in keywords) else 0
        conflict = 1 if (twitter + instagram + facebook) > 1 else 0

        #rows.append([date, title, extract_referenced_text(item)])
        rows.append([date, title])

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Title"])
        writer.writerows(rows)

    print("CSV file created successfully!")

# Usage example
json_file = "/home/ahsan/Downloads/pythonProject/custom_ner/data/ref_eng_formatted.json"
csv_file = "/home/ahsan/Documents/p/university/thesis/article_log/eng_testing_data.csv"
process_json_to_csv(json_file, csv_file)


