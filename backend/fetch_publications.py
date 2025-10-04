import pandas as pd
import requests
from bs4 import BeautifulSoup

def read_csv(csv_path):
    df = pd.read_csv(csv_path, sep="\t")
    return df.to_dict(orient="records")

def fetch_abstract(url):
    response = requests.get(url)
    if not response.ok:
        return ""
    soup = BeautifulSoup(response.text, 'html.parser')
    abstract_tag = soup.find('div', {'class': 'abstr'})
    if abstract_tag:
        return abstract_tag.get_text(strip=True)
    # Fallback for other page formats
    abstract_tag = soup.find('div', {'class': 'abstract'})
    if abstract_tag:
        return abstract_tag.get_text(strip=True)
    return ""