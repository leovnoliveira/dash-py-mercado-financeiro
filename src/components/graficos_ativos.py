import os
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.dash_py_mercado_financeiro.funcoes_dd import criando_grafico_acao
from src.dash_py_mercado_financeiro.app import *

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

path_ticker_csv = os.path.join(DATA_DIR, 'tickers.csv')

lista_empresas = pd.read_csv(path_ticker_csv)['tickers'].to_list()

layout = html.Div([dcc.Dropdown(lista_empresas, value = 'PETR4', id = 'escolher-grafico-aovivo',
                                className = 'dcc-padrao',
                                style= {'background-color': 'black', 'color': 'white'}),
                                
                                
                                dcc.Graph(style = {'width': '100%', 'height': '302px',
                                                   'margin-top': '16px',
                                                   'border-radius': '8px',
                                                   'background-color': '#131516',
                                                   'border': '2px solid #212946'}, id=  'grafico_candle')])

@callback(
    Output('grafico_candle', 'figure'),
    Input('escolher-grafico-aovivo', 'value')
)

def update_options(ticker):

    fig = criando_grafico_acao(ticker)

    return fig