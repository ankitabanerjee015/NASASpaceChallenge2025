import pandas as pd
import requests
from bs4 import BeautifulSoup

def read_csv(csv_path):
    df = pd.read_csv(csv_path, sep="\t")
    return df.to_dict(orient="records")

import requests
from bs4 import BeautifulSoup

def fetch_abstract(url):
    try:
        response = requests.get(url)
        if not response.ok:
            print("Request failed")
            return ""
        soup = BeautifulSoup(response.text, 'html.parser')
        print("HTML snippet:", response.text[:500])  # Debug: Show first 500 chars
        abstract_div = soup.find('div', class_='abstract')
        if abstract_div:
            paragraphs = abstract_div.find_all('p')
            if paragraphs:
                result = "\n".join([p.get_text(strip=True) for p in paragraphs])
                print("Abstract found (paragraphs):", result)
                return result
            result = abstract_div.get_text(strip=True)
            print("Abstract found (div):", result)
            return result
        print("No abstract div found")
    except Exception as e:
        print(f"Error fetching abstract for {url}: {e}")
    return ""

print(fetch_abstract("https://pmc.ncbi.nlm.nih.gov/articles/PMC11892206/"))
