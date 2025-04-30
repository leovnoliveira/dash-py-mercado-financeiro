from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from  io import StringIO
from datetime import timedelta
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

legenda = pd.Series(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                        index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])

#erro = 'NoSuchElementException'

def webscrapping_di() -> pd.DataFrame:

    datas_referencia = {
        'hoje': datetime.now(),
        'um_ano_atras': datetime.now() - timedelta(days=365),
        'tres_anos_atras': datetime.now() - timedelta(days=3 * 365),
        'cinco_anos_atras': datetime.now() - timedelta(days=5 * 365),
        'dez_anos_atras': datetime.now() - timedelta(days=10 * 365)
    }
    
    # lista_datas = [hoje, um_ano_atras, tres_anos_atras, cinco_anos_atras, dez_anos_atras]
    # lista_nomes = ['hoje', 'um_ano_atras', 'tres_anos_atras', 'cinco_anos_atras', 'dez_anos_atras']

    
    
    lista_dfs = []

    opcoes = Options()
    opcoes.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options= opcoes)

    for nome_periodo, data_pontual in datas_referencia.items():
        for tentativa in range(5):
            data_formatada = data_pontual.strftime("%d/%m/%Y")

            url = (
                f"https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?"
                f"pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&"
                f"Data={data_formatada}&Mercadoria=DI1"
            )

            try:
                tabela, indice = pegando_dados_di(url, driver)
                if tabela is not None and indice is not None:
                    dados_di = tratando_dados_di(tabela, indice)
                    dados_di = dados_di.reset_index()
                    dados_di.columns = ['data_vencimento', 'preco']
                    dados_di['data_preco'] = nome_periodo
                    lista_dfs.append(dados_di)
                    break
            except Exception as e:
                print(f'Erro ao acessar a URL ({data_formatada}): {e}')
                data_pontual -= timedelta(days = 1)

    driver.quit()

    if not lista_dfs:
        print("Nenhum dado foi coletado")
        return pd.DataFrame()
        
    dados_di = pd.concat(lista_dfs, ignore_index= True)
    dados_di.to_csv(os.path.join(DATA_DIR, "dados_di.csv"), index=False)

    return dados_di

def pegando_dados_di(url, driver):
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    elemento_tabela = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'body form table:nth-of-type(3) tr:nth-of-type(3) td:nth-of-type(3) table'))
    )
    elemento_indice = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body form table:nth-of-type(3) tr:nth-of-type(3) td:nth-of-type(1)'))
    )

    tabela_html = elemento_tabela.get_attribute('outerHTML')
    indice_html = elemento_indice.get_attribute('outerHTML')

    tabela = pd.read_html(StringIO(tabela_html))[0]
    indice = pd.read_html(StringIO(indice_html))[0]

    return tabela, indice

def tratando_dados_di(df_dados: pd.DataFrame, indice: pd.DataFrame) -> pd.Series:

    df_dados.columns = df_dados.loc[0]
    df_dados = df_dados.drop(0).set_index(indice.iloc[1:, 0])['ÚLT. PREÇO'].astype(int)

    df_dados = df_dados[df_dados != 0].astype(float) / 100000

    datas = [f"{legenda[idx[0]]}-{idx[1:3]}" for idx in df_dados.index]
    df_dados.index = datas

    return df_dados

if __name__ == '__main__':

    dados_di = webscrapping_di()
    print(dados_di)







