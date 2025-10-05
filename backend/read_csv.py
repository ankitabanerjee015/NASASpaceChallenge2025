import pandas as pd

def read_csv(path):
    df = pd.read_csv(path)
    publications = []
    for row in reader:
        # If the header came in merged, fix it here:
        if 'Title,Link' in row and ('Title' not in row or 'Link' not in row):
            combo = row['Title,Link']
            if isinstance(combo, str) and ',' in combo:
                title, link = combo.split(',', 1)
                row['Title'] = title.strip()
                row['Link'] = link.strip()
            # optional: del row['Title,Link']
        publications.append(row)
    return publications
