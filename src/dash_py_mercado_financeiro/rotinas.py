from dotenv import load_dotenv
from src.dash_py_mercado_financeiro.dados_b3 import composicao_ibov, setores_bolsa
from src.dash_py_mercado_financeiro.dados_di import webscrapping_di
from src.dash_py_mercado_financeiro.dados_mt5_cotacoes import construcao_historica_cotacoes, selecionando_tickers
from src.dash_py_mercado_financeiro.dados_bacen import att_divida_pib, att_dolar, att_inflacao
from src.dash_py_mercado_financeiro.dados_noticias import scraping_noticias
import time
import os

# Carregar variáveis de ambiente
load_dotenv()

while True:

    def atualizando_rotinas():


        caminho_downloads = os.getenv("caminho_downloads") # Caminho da sua pasta download, salvo em .env
        selecionando_tickers()
        construcao_historica_cotacoes()
        composicao_ibov(caminho_downloads=caminho_downloads)
        setores_bolsa(caminho_downloads=caminho_downloads)
        att_divida_pib()
        att_inflacao()
        att_dolar()
        webscrapping_di()
        scraping_noticias()

    atualizando_rotinas()

    time.sleep(60*60)