from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import time
from datetime import timedelta
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

#erro = 'NoSuchElementException'

def webscrapping_di() -> pd.DataFrame:

    hoje = datetime.now()
    um_ano_atras = hoje - timedelta(days = 365)
    tres_anos_atras = hoje - timedelta(days = 3*365)
    cinco_anos_atras = hoje - timedelta(days = 5*365)
    dez_anos_atras = hoje - timedelta(days = 10*365)
    
    lista_datas = [hoje, um_ano_atras, tres_anos_atras, cinco_anos_atras, dez_anos_atras]
    lista_nomes = ['hoje', 'um_ano_atras', 'tres_anos_atras', 'cinco_anos_atras', 'dez_anos_atras']

    legenda = pd.Series(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                        index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])
    
    lista_dfs = []


    for n, data in enumerate(lista_datas):
        opcoes = Options()
        opcoes.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)
        data_pontual = data
        tabela, indice = None, None

        for i in range(0, 5):

            data_teste = data_pontual.strftime('%d/%m/%Y')

            url = f'''https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?
            pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&Data={data_teste}&Mercadoria=DI1'''

            try:

                tabela, indice = pegando_dados_di(url, driver)

                break

            except Exception as e:

                print(f'Erro ao acessar a URL em {data_teste}: {e}')

            data_pontual = data_pontual - timedelta(days= 1)

        #driver.quit()

        if tabela is None or indice is None:
                print(f'Nenhum dado encontrado para {lista_nomes[n]}. Pulando...')
                continue

        dados_di = tratando_dados_di(tabela, indice, legenda)

        dados_di = dados_di.reset_index()
        dados_di.columns = ['data_vencimento', 'preco']
        dados_di['data_preco'] = lista_nomes[n]

        lista_dfs.append(dados_di)

    if len(lista_dfs) == 0:
        print('Nenhum dado foi coletado')
        return None
    
    dados_di = pd.concat(lista_dfs, ignore_index=True)
    dados_di_path_csv = os.path.join(DATA_DIR, "dados_di.csv")
    dados_di.to_csv(dados_di_path_csv, index = False)

    return dados_di

def pegando_dados_di(url, driver):

    sem_conexao = True
    
    while sem_conexao:
        try:
            driver.get(url)
            sem_conexao = False
        except:
            pass
    
    time.sleep(3)

    local_tabela = '''
    
    /html/body/form[1]/table[3]/tbody/tr[3]/td[3]/table
                    '''
    
    local_indice = '''
    
    /html/body/form[1]/table[3]/tbody/tr[3]/td[1]
                    '''
    
    elemento = driver.find_element('xpath', local_tabela)

    elemento_indice = driver.find_element('xpath', local_indice)

    html_tabela = elemento.get_attribute('outerHTML')
    html_indice = elemento_indice.get_attribute('outerHTML')

    tabela = pd.read_html(html_tabela)[0]
    indice = pd.read_html(html_indice)[0]

    return tabela, indice


def tratando_dados_di(df_dados: pd.DataFrame, indice, legenda: str):

    df_dados.columns = df_dados.loc[0]
    df_dados = df_dados['ÚLT. PREÇO']

    df_dados = df_dados.drop(0, axis = 0)

    indice.columns = indice.loc[0]

    indice_di = indice['VENCTO']

    indice = indice.drop(0, axis = 0)

    df_dados.index = indice['VENCTO']

    df_dados = df_dados.astype(int)

    df_dados = df_dados[df_dados != 0]

    df_dados = df_dados/1000

    lista_datas = []

    for indice in df_dados.index:

        letra = indice[0]
        ano = indice[1:3]
        mes = legenda[letra]
        data = f'{mes}-{ano}'
        #data = datetime.datetime.strftime(data, "%b-%y")

        lista_datas.append(data)

    df_dados.index = lista_datas
    df_dados = df_dados/100

    return df_dados


if __name__ == '__main__':

    dados_di = webscrapping_di()
    print(dados_di)







