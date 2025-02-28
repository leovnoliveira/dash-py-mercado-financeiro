from dados_b3 import composicao_ibov, setores_bolsa
from dados_di import webscrapping_di
from dados_mt5_cotacoes import construcao_historica_cotacoes, selecionando_tickers
from dados_bacen import att_divida_pib, att_dolar, att_inflacao
from dados_noticias import scraping_noticias
import time

while True:

    def atualizando_rotinas():


        caminho_downloads = r'C:\Users\Leonardo\Downloads'

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

    time.sleep(86400)