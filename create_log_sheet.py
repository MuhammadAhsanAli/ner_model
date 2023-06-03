import csv

# Create a CSV file
data = [
    ['Name', 'Facebook', 'Instagram', 'Twitter'],
    ['John', 'facebook.com/john', '', 'twitter.com/john'],
    ['Lisa', '', 'instagram.com/lisa', ''],
    ['Mike', '', '', 'twitter.com/mike'],
    ['Sarah', 'facebook.com/sarah', '', 'twitter.com/sarah']
]

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Read the CSV file and mark columns
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

    # Get the index of the title row
    title_row = rows[0]
    facebook_index = title_row.index('Facebook')
    instagram_index = title_row.index('Instagram')
    twitter_index = title_row.index('Twitter')

    # Mark columns based on conditions
    for row in rows[1:]:
        if 'facebook' in row[facebook_index]:
            row[facebook_index] = '1'
        else:
            row[facebook_index] = '0'

        if 'instagram' in row[instagram_index]:
            row[instagram_index] = '1'
        else:
            row[instagram_index] = '0'

        if 'twitter' in row[twitter_index]:
            row[twitter_index] = '1'
        else:
            row[twitter_index] = '0'

# Write the updated data back to the CSV file
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
