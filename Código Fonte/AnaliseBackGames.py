import pandas as pd
import numpy as np
import requests as res
from jogosdiabet import jogosdia
from AlertaTelegram import enviartip
import datetime

gameday = pd.read_excel('Base de Dados/JogosDoDia.xlsx')
#jogosdia()
results = []

def analisettback(jog1, jog2):
    
    #BASE DE DADOS JOGADORES + transformando para numpy
    df4 = pd.read_excel('Base de Dados/Base Jogadores/Jogadores.xlsx')
    df4 = df4.to_numpy()

    try:
            #Buscando codigo dos jogadores na planilha
        i = np.where(df4==jog1.title())[0][0]
        j = np.where(df4==jog2.title())[0][0]

        codjog1 = df4[i][0]
        codjog2 = df4[j][0]

    except:
        return None, None

    #ACESSOS URL
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome / 86.0.4240.198 Safari / 537.36"}
    try:
        urlJog1 = 'https://tt.league-pro.com/players/' + str(codjog1)
        urlJog2 = 'https://tt.league-pro.com/players/' + str(codjog2)
        urlH2H = 'https://tt.league-pro.com/statistics/' + urlJog1[34:] + '?vs=' + urlJog2[34:]

        dadosjog1 = res.get(urlJog1, headers=header)
        dadosjog2 = res.get(urlJog2, headers=header)
        dados2h2 = res.get(urlH2H, headers=header)
    except:
        return None, None
    
    #INFORMAÇÕES DOS JOGADORES

    def process_data(data):
        try:
            df = pd.read_html(data.text)
            if len(df) == 8:
                df = pd.concat([df[4], df[5], df[6], df[7]])
            else:
                df = pd.concat([df[4], df[5], df[6], df[7], df[8]])
            df = df.drop([0, 1, 4, 5, 8, 3], axis=1)
            df = df.drop([1, 0], axis=0)
            df.columns = ['Adversario', 'Placar', 'Sets']
            df[['P1', 'P2']] = df['Placar'].str.split(' : ', expand=True)
            df[['Set1', 'Set2', 'Set3', 'Set4', 'Set5']] = df['Sets'].str.split(' ', expand=True)
            df[['Set1', 'Set2', 'Set3', 'Set4', 'Set5']] = df[['Set1', 'Set2', 'Set3', 'Set4', 'Set5']].fillna('0-0')
            df[['PF1', 'PR1']] = df['Set1'].str.split('-', expand=True)
            df[['PF2', 'PR2']] = df['Set2'].str.split('-', expand=True)
            df[['PF3', 'PR3']] = df['Set3'].str.split('-', expand=True)
            df[['PF4', 'PR4']] = df['Set4'].str.split('-', expand=True)
            df[['PF5', 'PR5']] = df['Set5'].str.split('-', expand=True)
            df = df.drop(['Placar', 'Sets', 'Set1', 'Set2', 'Set3', 'Set4', 'Set5'], axis=1)
            for i in df:
                if i != 'Adversario':
                    df[i] = pd.to_numeric(df[i])
            return df
        except Exception as e:
            pass
        return None

    # INFO JOGADOR 1
    df = process_data(dadosjog1)
    # INFO JOGADOR 2
    df1 = process_data(dadosjog2)

    #ANALISE DOS JOGADORES 
    def calculate_stats(df):
        stats = {}

        try:
            # Totais sets
            df['TotalSets'] = df['P1'] + df['P2']

            # Média sets
            med_s = df['TotalSets'].sum() / len(df)
            stats['med_s'] = med_s

            # Porcentagem de over 3,5
            cont_over_3 = sum(1 for i in df['TotalSets'] if i > 3)
            over_3_percentage = (cont_over_3 / len(df)) * 100
            stats['over_3_percentage'] = over_3_percentage

            # Total Pontos 1 set
            df['Total1Set'] = df['PF1'] + df['PR1']
            med_p1s = df['Total1Set'].sum() / len(df)
            stats['med_p1s'] = med_p1s

            # Total Pontos 2 Set
            df['Total2Set'] = df['PF2'] + df['PR2']
            med_p2s = df['Total2Set'].sum() / len(df)
            stats['med_p2s'] = med_p2s

            # Vitórias 1 Set
            cont_w1 = sum(1 for i in df.itertuples(index=False) if i.PF1 > i.PR1)
            v1_percentage = (cont_w1 / len(df)) * 100
            stats['v1_percentage'] = v1_percentage

            # Vitórias 2 Set
            cont_w2 = sum(1 for i in df.itertuples(index=False) if i.PF2 > i.PR2)
            v2_percentage = (cont_w2 / len(df)) * 100
            stats['v2_percentage'] = v2_percentage

        except Exception as e:
            # Se ocorrer algum erro, imprime a mensagem de erro, mas continua a execução
            pass

        return stats

    # CONTAS JOGADOR 1
    stats_j1 = calculate_stats(df)
    # CONTAS JOGADOR 2
    stats_j2 = calculate_stats(df1)

    #CONTAS H2H

    df3 = pd.read_html(dados2h2.text)[0]
    def calculate_h2h_stats(df3):
        statsh2h = {}

        try:
            df3 = df3.drop(['Date', 'Tournaments', 'Rating tour', 'Rating opp', 'Delta','WP', 'LP', 'Total points'], axis=1)
            df3.columns = ['Placar', 'Sets']
            df3[['P1', 'P2']] = df3['Placar'].str.split(' : ',expand=True)
            df3[['Set1', 'Set2', 'Set3', 'Set4', 'Set5']] = df3['Sets'].str.split(' ', expand= True)
            df3[['Set1', 'Set2', 'Set3', 'Set4', 'Set5']] = df3[['Set1', 'Set2', 'Set3', 'Set4', 'Set5']].fillna('0-0')
            df3[['PF1', 'PR1']] = df3['Set1'].str.split('-', expand=True)
            df3[['PF2', 'PR2']] = df3['Set2'].str.split('-', expand=True)
            df3[['PF3', 'PR3']] = df3['Set3'].str.split('-', expand=True)
            df3[['PF4', 'PR4']] = df3['Set4'].str.split('-', expand=True)
            df3[['PF5', 'PR5']] = df3['Set5'].str.split('-', expand=True)
            df3 = df3.drop(['Placar', 'Sets', 'Set1', 'Set2', 'Set3', 'Set4','Set5'], axis=1)
            df3 = df3.drop(len(df3)-1, axis=0)
            for i in df3:
                if i != 'Adversario':
                    df3[i] = pd.to_numeric(df3[i])

            # Totais Sets
            df3['TotalSets'] = df3['P1'] + df3['P2']
            # Porcentagem de over 3,5
            cont_over_3 = sum(1 for i in df3['TotalSets'] if i > 3)
            Over3SetsH2h = (cont_over_3 / (len(df3)-1)) * 100
            statsh2h['Over3SetsH2h'] = Over3SetsH2h

            # Mais vitórias 1 set
            cont1_h2h = sum(1 for i in df3.itertuples(index=False) if i.PF1 > i.PR1)
            cont1l_h2h = sum(1 for i in df3.itertuples(index=False) if i.PF1 <= i.PR1)
            Vitoria1Set = jog1.title() if cont1_h2h > cont1l_h2h else jog2.title()
            statsh2h['Vitoria1Set'] = Vitoria1Set

            # Mais vitórias 2 set
            cont2_h2h = sum(1 for i in df.itertuples(index=False) if i.PF2 > i.PR2)
            contl2_h2h = sum(1 for i in df.itertuples(index=False) if i.PF2 <= i.PR2)
            Vitoria2Set = jog1.title() if cont2_h2h > contl2_h2h else jog2.title()
            statsh2h['Vitoria2Set'] = Vitoria2Set

            # Mais vitórias nas partidas
            contw_h2h = sum(1 for i in df3.itertuples(index=False) if i.P1 > i.P2)
            contl_h2h = sum(1 for i in df3.itertuples(index=False) if i.P1 <= i.P2)
            VencerPartida = jog1.title() if contw_h2h > contl_h2h else jog2.title()
            statsh2h['VencerPartida'] = VencerPartida

        except:
            pass
        
        return statsh2h
    
    statsh2h = calculate_h2h_stats(df3)

    try:
        result = {
            "Jogador1": jog1,
            "Jogador2": jog2,
            "Over3PercentageJ1": stats_j1["over_3_percentage"],
            "Over3PercentageJ2": stats_j2["over_3_percentage"],
            "Over3PercentageH2H": statsh2h["Over3SetsH2h"],
            "Med_S_J1": stats_j1["med_s"],
            "Med_S_J2": stats_j2["med_s"],
            "Med_P1S_J1": stats_j1["med_p1s"],
            "Med_P1S_J2": stats_j2["med_p1s"],
            "Med_P2S_J1": stats_j1["med_p2s"],
            "Med_P2S_J2": stats_j2["med_p2s"],
            "V1_Percentage_J1": stats_j1["v1_percentage"],
            "V1_Percentage_J2": stats_j2["v1_percentage"],
            "V2_Percentage_J1": stats_j1["v2_percentage"],
            "V2_Percentage_J2": stats_j2["v2_percentage"],
            "Vitoria1SetH2H": statsh2h["Vitoria1Set"],
            "Vitoria2SetH2H": statsh2h["Vitoria2Set"],
            "VencerPartidaH2H": statsh2h["VencerPartida"],
            "Link": urlH2H
        }
        results.append(result)

    except KeyError:
        pass

gameday = pd.read_excel('Base de Dados/JogosDoDia.xlsx')

jog1_column = gameday['Esquerda']
jog2_column = gameday['Direita']

for jog1, jog2 in zip(jog1_column, jog2_column):
    analisettback(jog1, jog2)

# Depois que o loop é concluído, crie um DataFrame a partir dos resultados coletados
results_df = pd.DataFrame(results)

# Salve o DataFrame em um novo arquivo Excel
results_df.to_excel(f"analysis_results{datetime.datetime.now()}.xlsx", index=False)
