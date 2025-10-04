import pandas as pd
import requests
from bs4 import BeautifulSoup

def read_csv(path: str):
    import csv
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Repair merged column, if present
            if "Title,Link" in row and ("Link" not in row):
                merged = row.get("Title,Link")
                if isinstance(merged, str) and "," in merged:
                    title, link = merged.rsplit(",", 1)
                    row["Title"] = title.strip().strip('"')
                    row["Link"] = link.strip()
            rows.append(row)
    return rows

def fetch_abstract(url):
    try:
        response = requests.get(url)
        if not response.ok:
            return ""
        soup = BeautifulSoup(response.text, 'html.parser')
        abstract_tag = soup.find('div', {'class': 'abstr'}) or soup.find('div', {'class': 'abstract'})
        if abstract_tag:
            return abstract_tag.get_text(strip=True)
    except Exception as e:
        print(f"Error fetching abstract for {url}: {e}")
    return ""
