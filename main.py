import re
from time import sleep
from func_covid import *
   
dados_mes_atual = dados(True)
dados_mes_anterior = dados()

dados_mes_anterior = organizaDados(dados_mes_anterior)
dados_mes_atual = organizaDados(dados_mes_atual)

dados_final = {"Mes_Atual": []}

for c, (m1, m2) in enumerate(zip(dados_mes_anterior["results"], dados_mes_atual["results"])):
    dados_final['Mes_Atual'].append({})
    for  (k, v1), (v2) in zip(m1.items(), m2.values()):
        if type(v1) == float:
            dados_final['Mes_Atual'][c][k] = 0
        elif type(v1) == int:
            if k in ["confirmed", "deaths"]:
                dados_final["Mes_Atual"][c][k] = v2 - v1
                if k == "deaths":
                    print(v2 , "-" , v1)
            else:
                dados_final['Mes_Atual'][c][k] = v2
        elif type(v1) == str or type(v1) == bool:
            dados_final['Mes_Atual'][c][k] = v2
    dados_final["Mes_Atual"][c]["confirmed_per_100k_inhabitants"] = round(dados_final["Mes_Atual"][c]["confirmed"] / dados_final["Mes_Atual"][c]["estimated_population"] * 100000, 5)
    dados_final["Mes_Atual"][c]["death_rate"] = round(dados_final["Mes_Atual"][c]["deaths"] / dados_final["Mes_Atual"][c]["confirmed"], 4)
    
for i, d in enumerate(dados_final['Mes_Atual']):
    for k, v in d.items():
        if i == 0:
            confirmados = d
            confirmados100k = d
            mediaMortes = d
            mortes = d
        else:
            if d["confirmed"] > confirmados["confirmed"]:
                confirmados = d
            if d["confirmed_per_100k_inhabitants"] > confirmados100k["confirmed_per_100k_inhabitants"]:
                confirmados100k = d
            if d["death_rate"] > mediaMortes["death_rate"]:
                mediaMortes = d
            if d["deaths"] > mortes["deaths"]:
                mortes = d

dadosCrit = {
            "confirmed": confirmados,
            "confirmed_per_100k_inhabitants": confirmados100k,
            "death_rate": mediaMortes,
            "deaths": mortes
            }

print("Dados do mês Atual: \n")
for i, (k, v) in enumerate(dadosCrit.items()):
    
    if i == 0:
        print(f"{v['state']} é o estado com maior número de casos confirmados, com {v['confirmed']} registrados.")
    elif i == 1:
        print(f"{v['state']} é o estado com maior média de casos por 100.000 habitantes, com uma média de {v['confirmed_per_100k_inhabitants']}.")
    elif i == 2:
        print(f"{v['state']} é o estado com maior média de mortes, com {v['death_rate']}.")
    elif i == 3:
        print(f"{v['state']} é o estado com maior número de mortes confirmadas, com {v['deaths']} registradas.")

    print(f"\tDados atualizados em {datetime.strptime(v['date'], '%Y-%m-%d').strftime('%d/%m/%Y')}")

print()
sleep(1)

while True:
    while True:
        user = str(input("Gostaria de ver os dados de algum mês espécifico? (S/N)")).upper().strip()
        if user in 'SN':
            break
        else:
            print("POR FAVOR INFORME UM VALOR VÁLIDO!")
    if user == 'N':
        break
    else:
        estado = str(input("Informe a UF do estado desejado: ")).upper().strip()
        estado = re.search(r"^(AC|AL|AM|AP|BA|CE|DF|ES|GO|MA|MG|MS|MT|PA|PB|PE|PI|PR|RJ|RN|RO|RR|RS|SC|SE|SP|TO)$", estado)
        if estado:
            print(f"Dados do estado {estado.group()}:\n")
            for dic in dados_final["Mes_Atual"]:
                if dic["state"] == estado.group():
                    for k, v in dic.items():
                        print(f"\t{k}: {v}")
            print()
            sleep(2)
        else:
            print("ESTADO NÃO ENCONTRADO!")
