# Vars de ambiente
import os
from dotenv import load_dotenv
load_dotenv()
dir = os.getenv('diretorio')
diretorio = os.path.join(dir, 'tickers.csv')
print(f"O diretorio onde está o arquivo tickers é: {diretorio}")
funcao_dd = os.getenv('diretorio_scripts')
app = os.getenv('diretorio_scripts')


import pandas as pd
from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sys
sys.path.append(funcao_dd)
from funcoes_dd import criando_grafico_acao
sys.path.append(app)
from app import *





lista_empresas = pd.read_csv(diretorio)['tickers'].to_list()

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