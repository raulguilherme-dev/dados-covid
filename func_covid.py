import requests
from datetime import datetime
from calendar import monthrange
from sys import exit

def mesAnterior(mes_atual):
    m = mes_atual[-2:]
    if m == '01':
        a = mes_atual[:4]
        a = int(a)
        a -= 1
        mes_anterior = str(a) + '-12'
    else:
        m = int(m)
        m -=1
        if len(str(m)) == 1:
            n = '0' + str(m)
        else:
            n = str(m)
        mes_lista = list(mes_atual)
        mes_lista[-2:] = n
        mes_anterior = "".join(mes_lista)
    return mes_anterior


def dados(is_last=False):
    
    token = '9d14a91841d80d42f055f9b656960f7fafb2ce33'
    head = {'Authorization': f'token {token}'}
    if is_last:
        op = f'is_last=True'
    else:
        mes_atual = datetime.today().strftime("%Y-%m")
        ano_mes = mesAnterior(mes_atual)
        dia = str(monthrange(int(ano_mes[:4]), int(ano_mes[-1]))[1])
        op = f'date={ano_mes}-{dia}'

    url = f'https://api.brasil.io/v1/dataset/covid19/caso/data/?place_type=state&{op}'
    resposta = requests.get(url, headers=head)
    
    if resposta.status_code == 200:
        print("OK")
        return resposta.json()
    else:
        print("Não foi possível consumir os dados da API")
        exit()


def organizaDados(dados_json):
    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR',
            'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    resultado = {"results": []}
    cont = 0
    print(dados_json)
    for c in dados_json["results"]:

        if c["state"] == estados[cont]:
            resultado['results'].append(c)
        else:
            for nc in dados_json["results"]:
                if nc["state"] == estados[cont]:
                    resultado['results'].append(nc)
        cont += 1
    return resultado
