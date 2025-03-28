import os
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.io as pio
from src.dash_py_mercado_financeiro.dados_mt5_cotacoes import pegando_todos_os_tickers, puxando_cotacoes

# Carregar diretório na raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) # ../../ p/ voltar duas pastas
DATA_DIR = os.path.join(BASE_DIR, "data")

# Carregar dados
cotacoes = os.path.join(DATA_DIR, 'cotacoes.parquet')
setores = os.path.join(DATA_DIR, 'setores.csv')
di = os.path.join(DATA_DIR, 'dados_di.csv')
dados_inflacao = os.path.join(DATA_DIR, 'inflacao.csv')
dados_dolar = os.path.join(DATA_DIR, 'dolar.csv')
dados_divida_pib = os.path.join(DATA_DIR, 'divida_pib.csv')


def criando_grafico_acao(acao):
        
        dados = pd.read_parquet(cotacoes, engine = 'fastparquet')
        dados['time'] = pd.to_datetime(dados['time'])
        dados = dados.set_index('time')
        acao_grafico = dados[dados['ticker'] == acao]

        acao_grafico = acao_grafico[acao_grafico.index > datetime.datetime.now() - datetime.timedelta(days = 1095)]

        layout = go.Layout(yaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False),
                           xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

        fig_ma = go.Figure(data=[go.Candlestick(x=acao_grafico.index,
                                            open=acao_grafico['open'], 
                                            high=acao_grafico['high'],
                                            low=acao_grafico['low'],
                                            close=acao_grafico['close']), 
                            ], layout=layout)

        fig_ma.update_layout(
            margin=dict(l=24, r=45, t=31, b=23), showlegend = False, font = dict(color = "#D3D6DF"))
        
        fig_ma.layout.plot_bgcolor = '#131516'
        fig_ma.update_layout(paper_bgcolor='rgba(0,0,0,0)')

        fig_ma.update_xaxes(tickcolor = '#131516', showgrid=False)
        fig_ma.update_yaxes(tickcolor = '#131516', showgrid=False)
        
        fig_ma.update_layout(xaxis_rangeslider_visible=False)

        return fig_ma


def tabela_cotacao_setor_bolsa(setor_escolhido):

    acoes_mt5 = pegando_todos_os_tickers()

    df_setores = pd.read_csv(setores)

    empresas_do_setor = df_setores[df_setores['SETOR'] == setor_escolhido]
    empresas_do_setor = empresas_do_setor['TICKER'].to_list()

    lista_tickers = [ticker for ticker in acoes_mt5 if ticker[:4] in empresas_do_setor] 
    lista_tickers = sorted(lista_tickers, reverse=True)
    lista_ticker_maior_liquidez = []

    for ticker in lista_tickers:

        if ticker[:4] + "4" not in lista_ticker_maior_liquidez:

            lista_ticker_maior_liquidez.append(ticker)

    cotacoes_ao_vivo = puxando_cotacoes(lista_ticker_maior_liquidez)

    cotacoes_ao_vivo = cotacoes_ao_vivo.dropna()

    return cotacoes_ao_vivo

def fazer_grafico_di(periodo):
        
        hoje = datetime.datetime.now() 
        
        dados_di = pd.read_csv(di)
        dados_di['data_vencimento'] = pd.to_datetime(dados_di['data_vencimento'], format = "%b-%y", errors = 'coerce')
        
        dados_atuais = dados_di[dados_di['data_preco'] == 'hoje']
        dados_atuais = dados_atuais.set_index('data_vencimento')
        dados_atuais = dados_atuais['preco']

        if periodo == '1 ano':
             
            dados_antigos = dados_di[dados_di['data_preco'] == 'um_ano_atras']
            data_antiga = hoje - datetime.timedelta(days = 365)
            data_antiga = data_antiga.strftime("%d/%m/%Y")
        
        elif periodo == '3 anos':
             
            dados_antigos = dados_di[dados_di['data_preco'] == 'tres_anos_atras']
            data_antiga = hoje - datetime.timedelta(days = 365 * 3)
            data_antiga = data_antiga.strftime("%d/%m/%Y")
        
        elif periodo == '5 anos':
             
            dados_antigos = dados_di[dados_di['data_preco'] == 'cinco_anos_atras']
            data_antiga = hoje - datetime.timedelta(days = 365 * 5)
            data_antiga = data_antiga.strftime("%d/%m/%Y")
        
        elif periodo == '10 anos':
             
            dados_antigos = dados_di[dados_di['data_preco'] == 'dez_anos_atras']
            data_antiga = hoje - datetime.timedelta(days = 365 * 10)
            data_antiga = data_antiga.strftime("%d/%m/%Y")
        
        dados_antigos = dados_antigos.set_index('data_vencimento')
        dados_antigos = dados_antigos['preco']
        
        hoje = hoje.strftime("%d/%m/%Y")

        layout = go.Layout(yaxis=dict(tickformat=".1%", tickfont=dict(color="#D3D6DF"), showline = False),
                            xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

        fig_di = go.Figure(layout=layout)

        fig_di.add_trace(go.Scatter(x=dados_atuais.index, y=dados_atuais.values, name=f"Curva {hoje}",
                                line=dict(color='firebrick', width=4), mode='lines+markers'))
        fig_di.add_trace(go.Scatter(x=dados_antigos.index, y=dados_antigos.values, name=f"Curva {data_antiga}",
                                line=dict(color='royalblue', width=4), mode='lines+markers'))

        fig_di.update_layout(
            margin=dict(l=60, r=48, t=24, b=36, autoexpand = False), legend=dict(x= 0.6, y=0.1, bgcolor = '#131516'), font = dict(color = "#D3D6DF"))

        fig_di.layout.plot_bgcolor = '#131516'
        fig_di.update_layout(paper_bgcolor='rgba(0,0,0,0)') #deixamos o paper transparante pra mudar o background no CSS e fazer border

        fig_di.update_xaxes(tickcolor = '#131516', showgrid=False)
        fig_di.update_yaxes(tickcolor = '#131516', showgrid=False)
        
        return fig_di

def fazer_tabela_di():

    df = pd.read_csv(di)
    df['data_vencimento'] = pd.to_datetime(df['data_vencimento'], format = "%b-%y", errors = 'coerce' )
    df = df[df['data_preco'] == 'hoje']
    df = df.set_index('data_vencimento')
    df = df['preco']

    hoje = datetime.datetime.now()
    ano_atual = hoje.year
    mes_atual = hoje.month

    DI_1Y = str(round(((df[df.index > datetime.datetime(ano_atual + 1, mes_atual, 1, 0, 0, 0)]).iloc[0] * 100), 2)) + "%" 
    DI_3Y = str(round(((df[df.index > datetime.datetime(ano_atual + 3, mes_atual, 1, 0, 0, 0)]).iloc[0] * 100), 2)) + "%" 
    DI_5Y = str(round(((df[df.index > datetime.datetime(ano_atual + 5, mes_atual, 1, 0, 0, 0)]).iloc[0] * 100), 2)) + "%" 
    DI_10Y = str(round(((df[df.index >= datetime.datetime(ano_atual + 10, 1, 1, 0, 0, 0)]).iloc[0] * 100), 2)) + "%" 

    df = pd.DataFrame({"ignore_1": ['DI 1Y', 'DI 3Y', 'DI 5Y', 'DI 10Y'], 'ignore_2': [DI_1Y, DI_3Y, DI_5Y, DI_10Y]})

    return df


def info_inflacao():
    
    inflacao = pd.read_csv(dados_inflacao)
    hoje = datetime.datetime.now()
    ano_atual = hoje.year
    inflacao = inflacao.set_index('Date')
    inflacao.index = pd.to_datetime(inflacao.index)

    inflacao = inflacao.iloc[-12:, :]
    inflacao_12m = (1 + inflacao).cumprod() - 1

    # Pega os dados apenas do ano atual
    inflacao_ano = inflacao.loc[str(ano_atual)]
    if inflacao_ano.empty:
        print("Não há dados de inflaçãp para o ano atual.")
        return pd.DataFrame() 
    
    # Se vier uma Series, transformar em DataFrame
    if isinstance(inflacao_ano, pd.Series):
        inflacao_ano = inflacao_ano.to_frame().T

    # Se houver NaN na última linha
    if pd.isna(inflacao.iloc[-1, 0]):
        inflacao.iloc[-1, 0] = inflacao.iloc[-2, 0]
    if pd.isna(inflacao.iloc[-1, 1]):
        inflacao.iloc[-1, 1] = inflacao.iloc[-2, 1]

    # Recalcular após os tratamentos
    inflacao_ano = (1 + inflacao_ano).cumprod() - 1
    inflacao_12m = (1 + inflacao).cumprod() - 1



    IPCA_12M = str(round((inflacao_12m.iloc[-1, 0] * 100), 2)) + "%"
    IGPM_12M = str(round((inflacao_12m.iloc[-1, 1] * 100), 2)) + "%"
    IPCA_ANO = str(round((inflacao_ano.iloc[-1, 0] * 100), 2)) + "%"
    IGPM_ANO = str(round((inflacao_ano.iloc[-1, 1] * 100), 2)) + "%"

    df = pd.DataFrame({"ignore_1": ["IPCA 12M", 'IGPM 12M', 'IPCA ANO', 'IGPM ANO'],
                       'ignore_2': [IPCA_12M, IGPM_12M, IPCA_ANO, IGPM_ANO]})

    return df

def grafico_inflacao(anos):

    pio.templates.default = "simple_white"
    
    inflacao = pd.read_csv(dados_inflacao)
    inflacao = inflacao.set_index('Date')
    inflacao.index = pd.to_datetime(inflacao.index)

    if anos == '1 ano':

        inflacao = inflacao.iloc[-12:, :]

    elif anos == '3 anos':

        inflacao = inflacao.iloc[-36:, :]
    
    elif anos == '5 anos':

        inflacao = inflacao.iloc[-60:, :]

    elif anos == '10 anos':

        inflacao = inflacao.iloc[-120:, :]

    layout = go.Layout(yaxis=dict(tickformat=".2%", tickfont=dict(color="#D3D6DF"), showline = False),
                        xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

    fig_infla = go.Figure(data=[
        go.Scatter(name='IPCA', x=inflacao.index, y=inflacao['ipca'], marker_color='firebrick'),
        go.Scatter(name='IGPM', x=inflacao.index, y=inflacao['igp-m'], marker_color='royalblue')
    ], layout=layout)

    fig_infla.add_shape( # add a horizontal "target" line
        type="line", line_color="white", line_width=3, opacity=1,
        x0=0, x1=1, xref="paper", y0=0, y1=0, yref="y"
    )
    fig_infla.update_layout(font = dict(color = "#D3D6DF"), margin=dict(l=24, r=45, t=31, b=23))
    
    fig_infla.layout.plot_bgcolor = '#131516'
    fig_infla.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    
    fig_infla.update_xaxes(tickcolor = '#131516')
    fig_infla.update_yaxes(tickcolor = '#131516')
    
    return fig_infla



def info_divida_pib():

    dados = pd.read_csv(dados_divida_pib)
    hoje = datetime.datetime.now()
    um_ano_atras = hoje - datetime.timedelta(days = 365)
    ano_passado = um_ano_atras.year
    dados = dados.set_index('Date')
    dados.index = pd.to_datetime(dados.index)
    
    dados = dados.iloc[-12:, :]

    VALOR_ATUAL = str(round((dados.iloc[-1, 0] * 100), 2)) + "%"
    VAR_12M = str(round((((dados.iloc[-1, 0] - dados.iloc[1, 0]) / dados.iloc[1, 0]) * 100), 2)) + "%" 
    VAR_ANO = str(round((((dados.iloc[-1, 0] - (dados.loc[f'{ano_passado}']).iloc[-1, 0]) / dados.loc[f'{ano_passado}'].iloc[-1, 0])  * 100), 2)) + "%"  
    VAR_MES = str(round((((dados.iloc[-1, 0] - dados.iloc[-2, 0]) / dados.iloc[-2, 0]) * 100), 2)) + "%"  

    df = pd.DataFrame({"ignore_1": ['VALOR ATUAL', 'Δ 12M', 'Δ ANO', 'Δ MÊS'], 'ignore_2': [VALOR_ATUAL, VAR_12M, VAR_ANO, VAR_MES]})

    return df



def grafico_divida_pib(anos):

    pio.templates.default = "simple_white"
    
    dados = pd.read_csv(dados_divida_pib)
    dados = dados.set_index('Date')
    dados.index = pd.to_datetime(dados.index)

    hoje = datetime.datetime.now()
    if anos == '1 ano':
        filtro_data = hoje - datetime.timedelta(days = 365)
    
    elif anos == '3 anos':

        filtro_data = hoje - datetime.timedelta(days = 365 * 3)
    
    elif anos == '5 anos':

        filtro_data = hoje - datetime.timedelta(days = 365 * 5)

    elif anos == '10 anos':

        filtro_data = hoje - datetime.timedelta(days = 365 * 10)

    else:
        filtro_data = dados.index.min() # Se nenhuma opção for válida, mostrar todos os dados

    dados_filtrados = dados[dados.index >= filtro_data]

    layout = go.Layout(yaxis=dict(tickformat=".2%", tickfont=dict(color="#D3D6DF"), showline = False),
                        xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

    fig_divida_pib = go.Figure(data=[
        go.Scatter(name='Dívida PIB', x=dados_filtrados.index, y=dados_filtrados['DIVIDA_PIB'], marker_color='royalblue')
    ], layout=layout)

    fig_divida_pib.update_layout(font = dict(color = "#D3D6DF"), margin=dict(l=24, r=45, t=31, b=23))
    
    fig_divida_pib.layout.plot_bgcolor = '#131516'
    fig_divida_pib.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    
    fig_divida_pib.update_xaxes(tickcolor = '#131516')
    fig_divida_pib.update_yaxes(tickcolor = '#131516')

    return fig_divida_pib


def info_dolar():

    dados = pd.read_csv(dados_dolar)
    dados['Date'] = pd.to_datetime(dados['Date'])
    hoje = datetime.datetime.now()
    ano_passado = hoje.year - 1
    dados = dados.set_index('Date')
    dados.index = pd.to_datetime(dados.index)

    um_ano_atras = hoje - datetime.timedelta(days = 365)
    data_mais_proxima_no_csv = dados.index.asof(um_ano_atras)


    # Verifica se encontrou a data
    if data_mais_proxima_no_csv is None:
        VAR_12M = "N/A"
    else:
        valor_12m_passado = dados.loc[data_mais_proxima_no_csv, dados.columns[0]]
        valor_atual = dados.iloc[-1, 0]

        VAR_12M = str(round(((valor_atual - valor_12m_passado) / valor_12m_passado) * 100, 2)) + "%"

    # Outras estatísticas
    VALOR_ATUAL = "R$" + str(round(dados.iloc[-1, 0], 2))


    dados_ano_passado = dados[dados.index.year == ano_passado]

    if not dados_ano_passado.empty:
        valor_ano_passado = dados_ano_passado.iloc[-1, 0]
        VAR_ANO = str(round(((dados.iloc[-1, 0] - valor_ano_passado) / valor_ano_passado) * 100, 2)) + "%"
    else:
        VAR_ANO = "N/A"

    VOL = str(round(((dados.pct_change().std().iloc[0] * 15.87) * 100), 2)) + "%"  

    df = pd.DataFrame({"ignore_1": ['VALOR ATUAL', 'Δ 12M', 'Δ ANO', 'VOL'],
                       'ignore_2': [VALOR_ATUAL, VAR_12M, VAR_ANO, VOL]})

    return df

def grafico_dolar(anos):

    pio.templates.default = "simple_white"
    
    dados = pd.read_csv(dados_dolar)
    dados = dados.set_index('Date')
    dados.index = pd.to_datetime(dados.index)

    if anos == '1 ano':

        dados = dados.iloc[-252:, :]

    elif anos == '3 anos':

        dados = dados.iloc[-(252 * 3):, :]
    
    elif anos == '5 anos':

        dados = dados.iloc[-(252 * 5):, :]

    elif anos == '10 anos':

        dados = dados.iloc[-(252 * 10):, :]

    layout = go.Layout(yaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False),
                        xaxis=dict(tickfont=dict(color="#D3D6DF"), showline = False))

    fig_dolar = go.Figure(data=[
        go.Scatter(name='Dólar', x=dados.index, y=dados['DOLAR'], marker_color='royalblue')
    ], layout=layout)

    fig_dolar.update_layout(font = dict(color = "#D3D6DF"), margin=dict(l=24, r=45, t=31, b=23))
    fig_dolar.update_layout(yaxis_tickprefix = 'R$', yaxis_tickformat = ',.2f')
    
    fig_dolar.layout.plot_bgcolor = '#131516'
    fig_dolar.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    
    fig_dolar.update_xaxes(tickcolor = '#131516')
    fig_dolar.update_yaxes(tickcolor = '#131516')

    return fig_dolar


























