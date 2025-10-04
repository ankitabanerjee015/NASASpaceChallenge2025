import pandas as pd

# Read CSV file from repo
csv_path = "publications.csv"
df = pd.read_csv(csv_path)

# Example: Print titles and links
for idx, row in df.iterrows():
    print(f"Title: {row['title']}, Link: {row['link']}")