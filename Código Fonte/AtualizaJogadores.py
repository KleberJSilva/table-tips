import requests
from bs4 import BeautifulSoup
import pandas as pd

def AtualizaJogadores():
    # Fazendo a requisição HTTP para obter o conteúdo da página
    url = 'https://tt.league-pro.com/players/?rat1=200&rat2=2000&rat=Search#list'
    response = requests.get(url)
    print(response)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Criando o objeto BeautifulSoup com o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrando a tabela na posição 0
        tables = soup.find_all('table')
        if len(tables) > 0:
            table = tables[0]

            # Encontrando todos os links na tabela
            links = table.find_all('a')

            # Criando uma lista para armazenar os dados dos links
            data = []

            # Iterando sobre os links
            for link in links:
                href = link.get('href')
                href_last_4 = href[-4:]  # Obtendo os 4 últimos dígitos do href
                link = link.text
                

                # Invertendo a posição das duas primeiras palavras
                words = link.split()
                if len(words) >= 2:
                    inverted_words = words[1] + ' ' + words[0] + ' ' + ' '.join(words[2:])
                    inverted_words = inverted_words.rstrip()
                    data.append([inverted_words, href_last_4])
                else:
                    pass

            # Criando um DataFrame com os dados
            df = pd.DataFrame(data, columns=['Jogador', 'Código'])

            # Criando um arquivo Excel com o DataFrame
            df.to_excel('Base de Dados/Base Jogadores/Jogadores.xlsx', index=False)
    else:
        print('Falha ao fazer a requisição HTTP')
AtualizaJogadores()        

