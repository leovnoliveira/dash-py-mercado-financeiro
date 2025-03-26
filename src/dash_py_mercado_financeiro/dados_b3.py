import pandas as pd
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
from datetime import timedelta
import zipfile
import os

# P/ acessar pasta './data'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) # p/ voltar duas pastas
DATA_DIR = os.path.join(BASE_DIR, "data")

def setores_bolsa(caminho_downloads):

    options = Options()
    options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm'

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "bvmf_iframe")))
    
    botao_expandir = driver.find_element('xpath', '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[1]/div/div/a/i')

    driver.execute_script("arguments[0].click();", botao_expandir)

    planilha = driver.find_element('xpath', '/html/body/app-root/app-companies-home/div/div/div/div/div[2]/div[2]/div/app-companies-home-filter-classification/form/div[2]/div[3]/div[2]/p/a')

    driver.execute_script("arguments[0].click();", planilha)

    time.sleep(5)

    driver.quit()

    caminho_zip = os.path.join(caminho_downloads + r"\ClassifSetorial.zip")

    with zipfile.ZipFile(caminho_zip) as arquivo_zip:
        # Para cada arquivo dentro do ZIP, garantimos que o objeto aberto seja fechado
        for planilha_nome in arquivo_zip.namelist():
            with arquivo_zip.open(planilha_nome) as file:
                setores = pd.read_excel(file, skiprows= 6, engine = 'openpyxl')

    # Funçõa par atentar remover o arquivo com retry
    def remove_file_with_retry(filepath: str, retries=5, delay=1):
        if not os.path.exists(filepath):
            print(f"Arquivo {filepath} não encontrado. Não é necessário remover.")
            return
        for i in range(retries):
            try:
                os.remove(filepath)
                print(f"Arquivo {filepath} removido com sucesso.")
                return
            except PermissionError:
                print(f"Tentativa {i+1} falhou ao tentar remover {filepath}. Tentar novamente")
                time.sleep(delay)
        raise PermissionError(f"Não foi possível remover o arquivo {filepath} após {retries} tentativas.")
    
    remove_file_with_retry(caminho_zip)

    # # agora com o zip fechado, podemos remove-lo sem problemas
    # os.remove(caminho_zip)

    setores['SUBSETOR'] = setores['SUBSETOR'].ffill()

    setores = setores.dropna(subset= ['SEGMENTO'])

    setores = setores[['SUBSETOR', 'SEGMENTO','LISTAGEM' ]]

    setores = setores.dropna()

    setores.columns = ['SETOR', 'NOME', 'TICKER']

    path_csv_setores = os.path.join(DATA_DIR, "setores.csv")

    setores.to_csv(path_csv_setores, index = False)



def composicao_ibov(caminho_downloads):

    options = Options()
    options.headless = False
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm'

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID,  "bvmf_iframe"))
    )

    time.sleep(3)

    planilha = driver.find_element("xpath", '//*[@id="divContainerIframeB3"]/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a')

    driver.execute_script("arguments[0].click();", planilha)

    time.sleep(5)

    driver.quit()

    # ============================================
    # Lógica para avançar a data até 5 tentativas
    # ============================================


    dt = date.today()
    ibovespa_comp = None
    arquivo_encontrado = False

    for attempt in range(5):
         # Se dt cair num fim de semana (sábado=5 ou domingo=6), pule para a próxima segunda
        if dt.weekday() >= 5:
            dias_para_segunda = 7 - dt.weekday()
            dt += timedelta(days=dias_para_segunda)

      
        dia = dt.strftime("%d")
        mes = dt.strftime("%m")
        ano = dt.strftime("%y")

        nome_arquivo = f"IBOVDia_{dia}-{mes}-{ano}.csv"
        caminho_csv = os.path.join(caminho_downloads, nome_arquivo)
        print(f"Tentativa {attempt+1}: procurando o arquivo {nome_arquivo}")

        try:
            ibovespa_comp = pd.read_csv(
                caminho_csv,
                sep=';',
                skipfooter=2,
                encoding='ISO-8859-1',
                engine='python',
                decimal=',',
                thousands='.',
                header=1,
                index_col=False
            )
            # Se deu certo, remove o arquivo do path de downloads
            os.remove(caminho_csv)
            arquivo_encontrado = True
            print(f"Arquivo encontrado: {nome_arquivo}")
            break

        except FileNotFoundError:
            print(f"Arquivo não encontrado para a data {dt.strftime('%d-%m-%y')}. Tentando o próximo dia útil...")
            dt += timedelta(days=1)

    # Se depois de 5 tentativas não encontrou, lança erro
    if not arquivo_encontrado or ibovespa_comp is None:
        raise FileNotFoundError("Não foi possível encontrar o arquivo IBOVDia nos próximos 5 dias úteis.")
        

        # --------------------------------------------
        # Continuação do código de tratamento do DataFrame
        # --------------------------------------------
    ibovespa_comp.columns = ['codigos', 'nome', 'classe', 'qtd', 'part']
            
    caminho_comp_csv = os.path.join(DATA_DIR, "comp_ibov.csv")
    ibovespa_comp.to_csv(caminho_comp_csv, index=False)


if __name__ == "__main__":

    load_dotenv()

    # Acesse seu path padrão de downloads
    caminho_downloads = os.getenv("caminho_downloads") # Path informado dentro do .env

    composicao_ibov(caminho_downloads)
    setores_bolsa(caminho_downloads)