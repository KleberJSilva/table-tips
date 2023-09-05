import pandas as pd
import requests
from bs4 import BeautifulSoup

def jogosdia():
    base_url = 'https://bsportsfan.com/ls/22742/Czech-Liga-Pro//p.'
    all_dados_esquerda = []
    all_dados_direita = []
    all_dados_data = []

    for page_number in range(1, 5):
        url = f'{base_url}{page_number}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table_element = soup.find('table', class_='table-sm')
        dados = []

        for td_element in table_element.find_all('td'):
            dados.append(td_element.get_text())

        dados_esquerda = []
        dados_direita = []
        dados_data = []

        for i, dado in enumerate(dados):
            if i % 4 == 0:
                dados_data.append(dado)
            else:
                partes = dado.split(" v ")
                if len(partes) == 2:
                    parte_esquerda, parte_direita = partes
                    dados_esquerda.append(parte_esquerda.strip())
                    dados_direita.append(parte_direita.strip())

        all_dados_esquerda.extend(dados_esquerda)
        all_dados_direita.extend(dados_direita)
        all_dados_data.extend(dados_data)

    df = pd.DataFrame({'Esquerda': all_dados_esquerda, 'Direita': all_dados_direita, 'Data': all_dados_data})
    df = df.dropna()
    df.to_excel('Base de Dados/JogosDoDia.xlsx', index=False)

# Chamar a função para iniciar o processo
jogosdia()

