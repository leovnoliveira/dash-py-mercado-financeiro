import pandas as pd
import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")


def pegando_todos_os_tickers():

    """
    Inicializa o MetaTrader5 e obtém todos os tickers listados.
    Faz uma filtragem para retornar apenas as ações (e units) brasileiras.

    """

    # 1) Inicia a conexão com o MT5
    
    if not mt5.initialize():
         print("initialize() failed, error code =", mt5.last_error())
         return []
    
    
    # 3) Pega todos os símbolos disponíveis:
    simbolos = mt5.symbols_get()
    tickers = [simbolo.name for simbolo in simbolos]
    tickers = sorted(tickers, reverse=True)

    acoes = []

    for ticker in tickers:
      # Exemplo de checagem para ver se a 4ª letra é um dígito
        try:
            int(ticker[3]) #a quarta letra tem que ser uma string, não um número. se não for dígito, cairá no except
        except:
            
            final_ticker = ticker[4:]

            if len(final_ticker) == 2:
                # Checa se final é "11" (units) ou "3"/"4" (ON/PN)
                if final_ticker == "11":

                    if (ticker[0:4] + "3") in acoes or (ticker[0:4] + "4") in acoes:

                        acoes.append(ticker)

            if len(final_ticker) == 1:  

                if final_ticker == "3" or final_ticker == "4":

                    acoes.append(ticker)

    return acoes    


def gerar_lista_principais():
    """
    Retorna uma lista com alguns ativos principais (mini índice, mini dólar, SMAL11, IVVB11 e DI futuro).
    """

    """
    O vencimento do contrato de dólar acontece no primeiro dia útil de todo mês.
    Já o vencimento do contrato de índice acontece a cada dois meses (somente nos meses pares).
    """

    legenda_indice = pd.Series([2, 4, 6, 8, 10, 12],
                        index = ['G', 'J', 'M', 'Q', 'V', 'Z'])
    
    legenda_dolar = pd.Series(list(range(1, 13)),
                        index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])
    
    ano = datetime.datetime.now().year
    mes = datetime.datetime.now().month

    if mes == 12:

        letra_indice = 'G'
        letra_dolar = 'F'
        codigo_indice = 'WIN' + letra_indice + str(ano + 1)[2:]
        codigo_dolar = 'WDO' + letra_dolar + str(ano + 1)[2:]
    
    else:
         
        letra_indice = (legenda_indice[legenda_indice > mes]).index[0]
        letra_dolar = (legenda_dolar[legenda_dolar > mes]).index[0]

        codigo_indice = 'WIN' + letra_indice + str(ano)[2:]
        codigo_dolar = 'WDO' + letra_dolar + str(ano)[2:]

    tickers_juros = [f"DI1F{str(ano_escolhido)[2:]}" for ano_escolhido in range(ano + 1, ano + 6)] 

    tickers_mercado = [codigo_indice, codigo_dolar, 'SMAL11', 'IVVB11'] + tickers_juros

    return tickers_mercado


def selecionando_tickers():
         
    """
    Exemplo de função que seleciona todos os tickers (ações + principais).
    Mostra como chamar 'symbol_select' e checar se o símbolo foi selecionado.
    """

    acoes = pegando_todos_os_tickers()
    tickers_mercado = gerar_lista_principais()
    
    tickers_totais = acoes + tickers_mercado

    for ticker in tickers_totais:
            # Tenta selecionar o símbolo
            selected = mt5.symbol_select(ticker, True)
            if not selected:
                print(f"Falha ao selecionar/acessar o símbolo: {ticker}")
            else:
                # Se quiser, podemos checar se há ticks (symbol_info_tick)
                if mt5.symbol_info_tick(ticker) is None:
                    print(f"Ticker {ticker} não possui tick info (pode estar indisponível).")


def puxando_cotacoes(tickers_escolhidos: list, principal = False):
    """
    Monta um DataFrame com [Ticker, Preço, Retorno] para cada ticker.
    Faz checagens para evitar AttributeError quando symbol_info(ticker) == None.
    """

    # 1) Checa se está conectado
    if not mt5.initialize():
        print("Não está conectado ao MetaTrader 5. Chame a mt5.initialize() antes")
        return pd.DataFrame(columns=['Ticker', 'Preço', 'Retorno'])
    
    df_cotacoes = pd.DataFrame(columns=['Ticker', 'Preço', 'Retorno'], index=range(len(tickers_escolhidos)))
    df_cotacoes = df_cotacoes.dropna(subset= "Preço")

    for i, ticker in enumerate(tickers_escolhidos):

        if principal == False:
            # 2) Tenta selecionar o símbolo antes de acessar info
            if mt5.symbol_info(ticker).session_deals > 10:
                print(f"Não foi possível selecionar o ticker: {ticker}")
                continue

            info = mt5.symbol_info(ticker)
            if info is None:
                print(f"symbol_info retornou None para {ticker} - símbolo inexistente ou indisponível.")
                continue

            # 3) Finalmente, acessmos os atributos (retorno e preço)

            retorno = info.price_change
            fechamento = info.last

            df_cotacoes.loc[i, :] = [ticker, fechamento, retorno]

    # Opcional: remover linhas que não foram preenchidas (NaN)
    df_cotacoes = df_cotacoes.dropna(subset=['Preço'], inplace= True)
           
    return df_cotacoes


def maiores_altas(tickers_ibov: list):
    """
    Exemplo de função que pega as maiores altas entre as ações do IBOV.
    """
        
    acoes = pegando_todos_os_tickers()

    df = puxando_cotacoes(acoes)

    # filtra só tickers do ibov
    df = df[df['Ticker'].isin(tickers_ibov)]

    # ordena e pega top 3

    df = df.sort_values("Retorno", ascending = False)
    df = df.head(3)
    df = df.reset_index(drop = True)

    return df

def maiores_baixas(tickers_ibov: list):
    """
    Exemplo de função que pega as maiores baixas entre as ações do IBOV.
    """

    acoes = pegando_todos_os_tickers()
    df = puxando_cotacoes(acoes)
    
    # filtra só tickers do ibov
    df = df[df['Ticker'].isin(tickers_ibov)]

    # ordena e pega o top 3
    df = df.sort_values("Retorno", ascending = True)
    df = df.head(3)
    df = df.reset_index(drop = True)

    return df


def construcao_historica_cotacoes():
    """
    Exemplo de coleta de dados históricos diários (D1) para as ações.
    Salva em .parquet usando fastparquet, com verificação de datas.
    """
    
    acoes = pegando_todos_os_tickers()
    lista_df_cotacoes = []
    timezone = pytz.timezone("Brazil/West")
    data_inicial = (datetime.datetime.now(tz = timezone) - datetime.timedelta(days= 1095))
    data_final = datetime.datetime.now(tz = timezone)

    for acao in acoes:

        try:

            cotacoes = mt5.copy_rates_range(acao, mt5.TIMEFRAME_D1, data_inicial, data_final)

            if cotacoes is None:
                print(f"Não foi possível coletar dados para a ação {acao}")
                continue

            df_temp = pd.DataFrame(cotacoes)
            
            df_temp = df_temp[['time', 'open', 'high', 'low', 'close']]
            df_temp['time']=pd.to_datetime(df_temp['time'], unit='s')
            df_temp['ticker'] = acao

            lista_df_cotacoes.append(df_temp)

        except Exception as e:
             
             print(f"Erro ao processar {acao}: {e}")

    if not lista_df_cotacoes:
        print("Nenhum dado foi coletado")

        return

    cotacoes_finais = pd.concat(lista_df_cotacoes, ignore_index= True)

    empresas = cotacoes_finais['ticker'].unique()
    df_empresas = pd.DataFrame({'tickers': empresas})

    df_empresas.to_csv(os.path.join(DATA_DIR, 'tickers.csv'), index = False)
    cotacoes_finais.to_parquet(os.path.join(DATA_DIR, "cotacoes.parquet"), engine = 'fastparquet', index = False) 



if __name__ == "__main__":

    # Exemplo de uso
    todas_as_acoes = pegando_todos_os_tickers()
    print("Ações filtradas:", todas_as_acoes)

    indices = gerar_lista_principais()

    tabela = puxando_cotacoes(tickers_escolhidos=[todas_as_acoes, indices])
    print("Cotação de IVVB11 e SMAL11:\n", tabela)

    # Exemplo de construção do histórico
    construcao_historica_cotacoes()

























