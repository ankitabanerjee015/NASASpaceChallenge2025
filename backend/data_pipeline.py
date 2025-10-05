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

import re

def fetch_abstract(url):
    import re
    import requests
    from bs4 import BeautifulSoup

    m = re.search(r'/PMC(\d+)', url)
    if not m:
        print("No PMC ID found in URL:", url)
        return ""
    pmcid = f"PMC{m.group(1)}"
    # Try Europe PMC first
    api_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={pmcid}&format=json"
    response = requests.get(api_url)
    if response.ok:
        data = response.json()
        results = data.get("resultList", {}).get("result", [])
        if results:
            abstract = results[0].get("abstractText", "")
            if abstract:
                print(f"Got abstract from Europe PMC for {pmcid}")
                return abstract
    # Fallback: NCBI PMC HTML scraping
    try:
        print(f"Trying NCBI PMC scraping for {url}")
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        # 1. Try <div id="abstract">
        abstract_div = soup.find("div", id="abstract")
        if abstract_div:
            # Get all <p> tags inside
            paragraphs = abstract_div.find_all("p")
            if paragraphs:
                text = "\n".join([p.get_text(strip=True) for p in paragraphs])
                print(f"Got abstract paragraphs from <div id='abstract'> for {pmcid}")
                return text
        # 2. Try any <p> tag whose id starts with "Par"
        abstract_pars = soup.find_all("p", id=re.compile("^Par"))
        if abstract_pars:
            text = "\n".join([p.get_text(strip=True) for p in abstract_pars])
            print(f"Got abstract from <p id='Par...'> for {pmcid}")
            return text
        # 3. Fallback: Try <div class="abstr"> and <div class="abstract">
        abstract_div = soup.find("div", class_="abstr") or soup.find("div", class_="abstract")
        if abstract_div:
            text = abstract_div.get_text(strip=True)
            print(f"Got abstract from <div class='abstr'/'abstract'> for {pmcid}")
            return text
        print(f"No abstract found in NCBI PMC page for {pmcid}")
    except Exception as e:
        print(f"NCBI fallback error for {url}: {e}")
    print(f"No abstract found for {pmcid}")
    return ""
