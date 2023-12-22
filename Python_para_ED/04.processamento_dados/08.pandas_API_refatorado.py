import pandas as pd
import requests, logging

from datetime import datetime as dt

# parte 1 - função para extrair as informações do site a partir do código do produto (str)

def extracao_dados(cod_produto:str):
    
    url = 'https://world.openfoodfacts.org/api/v2/product/'
    url_completa = url + cod_produto
    resposta = requests.get(url_completa)

    dados_brutos = resposta.json()

    return dados_brutos

# parte 2 - criando um dataframe com as colunas de nosso interesse a partir dos dados brutos que obtivemos no requests.get 

def selecionar_colunas(dados_brutos):

    dados_produto = dados_brutos.get('product', None)
    dados = pd.json_normalize(dados_produto) # transformando o json em dataframe, bidimensional (LXC)
    
    dados_target = dados[['_id', 'product_name', 'brands', 'created_t', 'image_front_small_url']] # selecionando colunas de nosso interesse

    return dados_target # aqui, retornamos um dataframe com as colunas que nos interessam

# parte 3 - agora, vamos incluir algumas colunas e ver se precisamos fazer alguma transformação nos dados que já obtivemos

def modelagem_final(dados_target:pd.DataFrame):
    # primeiro: converter a coluna created_t para o formato datetime em data
    dados_target['created_t'] = pd.to_datetime(dados_target['created_t'], unit='s')
    # depois: incluir coluna com a data de inclusão do registro no dataframe
    dados_target['data_registro'] = dt.now().strftime('%d/%m/%Y %H:%M:%S')


    return(dados_target)

# parte 4 - para fechar, vamos agora criar uma função para salvar o dataframe em um csv

def salvar_dados_em_csv(dados_target):

    dados_target.to_csv(f'{caminho_arquivo}{nome_arquivo}', index=False)



if __name__ == '__main__':

    # vamos primeiro informar as variáveis que precisam ser declaradas antes de chamarmos as funções:

    cod_produto = '7891000369371' # código do produto de que desejamos extrair as infos
    nome_arquivo = 'registro_openfood.csv' # nome para salvar o arquivo
    caminho_arquivo = '/home/lula/Trilha_ED/Python_para_ED/04.processamento_dados/dados/bronze/csv/' # parta em que será salvo o arquivo

    dados_brutos = extracao_dados(cod_produto) # chamando a parte 1, para extrair os dados a partir do cód de produto informado
    status_code = dados_brutos.get('status_verbose') # agora vamos incluir uma verificação se o cód do produto foi encontrado

    if status_code == 'product found':
        dados_target = selecionar_colunas(dados_brutos) # chamando a parte 2, para criar um df com as colunas que nos interessam
        dados_target = modelagem_final(dados_target) # chamando a parte 3, para incluir colunas/modificar dados existentes


        try:
            salvar_dados_em_csv(dados_target)
            logging.warning(f'Arquivo escrito com sucesso: {nome_arquivo} salvo em {caminho_arquivo}')

        except Exception as e:
            logging.warning(f'Falha ao escrever arquivo: {nome_arquivo}')
            logging.warning(f'Erro: {e}')

    else:
        logging.warning(f'Status: {status_code}')







