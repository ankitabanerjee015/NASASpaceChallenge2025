import csv
import requests

def read_publications(csv_path):
    publications = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['title']
            link = row['link']
            # Fetch abstract or full text from link (simplified)
            response = requests.get(link)
            if response.ok:
                content = extract_abstract(response.text)  # Define this function as needed
                publications.append({'title': title, 'link': link, 'content': content})
    return publications