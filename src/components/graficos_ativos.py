import os
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from src.dash_py_mercado_financeiro.app import *
from src.dash_py_mercado_financeiro.funcoes_dd import criando_grafico_acao

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

path_csv_tickers = os.path.join(DATA_DIR, "tickers.csv")

lista_empresas = pd.read_csv(path_csv_tickers)['tickers'].to_list()

layout = html.Div([dcc.Dropdown(lista_empresas, value = 'PETR4', id = 'escolher-grafico-aovivo', className = 'dcc-padrao',
                                                        style = {"background-color": 'black', 'color': 'white'}),
                                                        
                                dcc.Graph( style={"width": "100%", 'height': "302px", 'margin-top': '16px', 
                                                             'border-radius':'8px', 
                                                             'background-color': '#131516', 'border': "2px solid #212946"}, id ='grafico_candle')])

@app.callback(
    Output('grafico_candle', 'figure'),
    Input('escolher-grafico-aovivo', 'value'),
    prevent_initial_call=True
)
def update_options(ticker):
    print(f"Callback ativado para o ativo: {ticker}")
    

    fig = criando_grafico_acao(ticker)

    return {'data': [], 'layout': {}}, fig






















