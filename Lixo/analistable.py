import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

base_url = "https://bsportsfan.com/le/22742/Czech-Liga-Pro/p."
table_class = "table table-sm"
data = []

for i in range(1, 100):
    url = base_url + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_=table_class)
        if table:
            rows = table.find_all("tr")
            for row_index, row in enumerate(rows):
                if row_index == 0:
                    continue  # Ignore the first row
                cols = row.find_all(["th", "td"])
                row_data = [
                    col.get_text(strip=True).replace(
                        "\xa0v\xa0", ";"
                    )
                    if "\xa0v\xa0" in col.get_text()
                    else col.get_text(strip=True)
                    for col in cols
                ]
                data.append(row_data)
        else:
            print(f"No table found on page {i}\n")
    else:
        print(f"Failed to fetch page {i} (status code: {response.status_code})\n")

# Convert data to a DataFrame
df = pd.DataFrame(data)

def separar_texto(df):
    padrao = re.compile(r'([a-z])v([A-Z])')
    resultado = re.sub(padrao, r'\1 v \2', df)
    return resultado

games = []

for i in df['Games']:
    df1 = separar_texto(i)
    games.append(df1)

df1 = pd.DataFrame(games)

df1.to_excel('x.xlsx', index=False)

