import os
import datetime
import pandas as pd
import pytz
import yfinance as yf
import logging

# Define os diretórios base (subindo dois níveis para chegar à raiz do projeto)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Define e cria o diretório de logs (se não existir)
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "erros_yfinance.txt")

# Configuração do logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s",
    filemode='a'
)

def pegando_todos_os_tickers():
    """
    Lê os tickers a partir do arquivo CSV (presumivelmente sem sufixo) e acrescenta ".SA".
    Caso o arquivo não seja encontrado, retorna uma lista padrão.
    """
    path_tickers_csv = os.path.join(DATA_DIR, 'tickers.csv')
    
    try:
        df = pd.read_csv(path_tickers_csv)
        # Supondo que a coluna no CSV se chame 'tickers'
        tickers = df['tickers'].dropna().astype(str).tolist()
    except Exception as e:
        logging.error(f"Erro ao ler tickers do CSV: {e}")
        tickers = ["PETR4", "VALE3", "ITUB4", "B3SA3"]  # fallback
    
    # Acrescenta o sufixo ".SA" se ainda não estiver presente
    tickers_formatados = [ticker.strip() + ("" if ticker.strip().endswith(".SA") else ".SA") for ticker in tickers]
    return tickers_formatados

def gerar_lista_principais():
    """
    Gera uma lista com tickers principais disponíveis no Yahoo Finance.
    Exemplo:
      - Ibovespa: ^BVSP
      - Dólar/Real: USDBRL=X
      - ETFs: SMAL11.SA, IVVB11.SA
    """
    tickers_mercado = ["^BVSP", "USDBRL=X", "SMAL11.SA", "IVVB11.SA"]
    return tickers_mercado

def puxando_cotacoes(tickers_escolhidos: list, principal=False):
    """
    Para cada ticker em tickers_escolhidos, utiliza yfinance para obter as cotações atuais.
    Usa o atributo `info` para obter o preço (regularMarketPrice) e a variação (regularMarketChangePercent).
    Se o ticker não retornar dados válidos, gera um log de erro.
    """
    df_cotacoes = pd.DataFrame(columns=['Ticker', 'Preço', 'Retorno'])
    
    for ticker in tickers_escolhidos:
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            # Se info estiver vazio ou sem o preço, levanta exceção
            if not info or info.get('regularMarketPrice') is None:
                raise ValueError("Dados inválidos")
            preco = info.get('regularMarketPrice')
            retorno = info.get('regularMarketChangePercent')
            
            df_cotacoes = df_cotacoes.append({
                'Ticker': ticker,
                'Preço': preco,
                'Retorno': retorno
            }, ignore_index=True)
        except Exception as e:
            error_msg = f"Não existe o ticker {ticker} dentro do Yahoo Finance"
            logging.error(error_msg)
            # Opcionalmente, você pode continuar (não adiciona nada ao dataframe)
            continue
            
    return df_cotacoes

def maiores_altas(tickers_ibov: list):
    """
    Filtra os tickers presentes em tickers_ibov, ordena pelo retorno (variação percentual)
    e retorna os 3 com maiores altas.
    """
    acoes = pegando_todos_os_tickers()
    df = puxando_cotacoes(acoes)
    df = df[df['Ticker'].isin(tickers_ibov)]
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df.sort_values("Retorno", ascending=False)
    df = df.head(3).reset_index(drop=True)
    return df

def maiores_baixas(tickers_ibov: list):
    """
    Filtra os tickers presentes em tickers_ibov, ordena pelo retorno
    e retorna os 3 com maiores baixas.
    """
    acoes = pegando_todos_os_tickers()
    df = puxando_cotacoes(acoes)
    df = df[df['Ticker'].isin(tickers_ibov)]
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df.sort_values("Retorno", ascending=True)
    df = df.head(3).reset_index(drop=True)
    return df

def construcao_historica_cotacoes():
    """
    Obtém dados históricos de cada ticker utilizando yfinance.
    Salva os tickers disponíveis e o histórico consolidado.
    """
    tickers = pegando_todos_os_tickers()
    lista_df_cotacoes = []
    
    # Define o intervalo histórico (ex.: últimos 3 anos)
    data_inicial = datetime.datetime.now() - datetime.timedelta(days=1095)
    data_final = datetime.datetime.now()
    
    for ticker in tickers:
        try:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(start=data_inicial, end=data_final)
            if hist.empty:
                logging.error(f"Sem dados históricos para {ticker}")
                continue
            hist.reset_index(inplace=True)
            # Seleciona e renomeia as colunas
            hist = hist[['Date', 'Open', 'High', 'Low', 'Close']]
            hist.rename(columns={'Date':'time', 'Open':'open', 'High':'high', 'Low':'low', 'Close':'close'}, inplace=True)
            hist['ticker'] = ticker
            lista_df_cotacoes.append(hist)
        except Exception as e:
            logging.error(f"Erro com o ticker {ticker}: {e}")
    
    if lista_df_cotacoes:
        cotacoes_finais = pd.concat(lista_df_cotacoes)
        empresas = cotacoes_finais['ticker'].unique()
        df_empresas = pd.DataFrame({'tickers': empresas})
        df_empresas.to_csv(os.path.join(DATA_DIR, 'tickers.csv'), index=False)
        cotacoes_finais.to_parquet(os.path.join(DATA_DIR, "cotacoes.parquet"), index=False)
    else:
        logging.error("Nenhum dado histórico foi obtido.")

if __name__ == "__main__":
    # Exemplo de uso:
    todos_tickers = pegando_todos_os_tickers()
    print("Tickers obtidos:", todos_tickers)
    
    # Obtém cotações ao vivo para alguns tickers principais
    tickers_mercado = gerar_lista_principais()
    tabela = puxando_cotacoes(tickers_escolhidos=tickers_mercado, principal=True)
    print("Cotações principais:", tabela)
    
    # Constrói o histórico e salva os arquivos
    construcao_historica_cotacoes()
