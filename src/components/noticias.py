# Vars de ambiente
import os
from dotenv import load_dotenv
load_dotenv()
dir = os.getenv('diretorio')
diretorio = os.path.join(dir, 'noticias.csv')
app = os.getenv('diretorio_scripts')


import sys
sys.path.append(app)
from src.dash_py_mercado_financeiro.app import *
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, callback
import pandas as pd
from dash.dependencies import Input, Output

lista_jornais_br = ['G1', 'Valor Econômico', 'Brazil Journal']
lista_jornais_gringos = ['WSJ', 'Financial Times', 'Fortune 500']

layout_brasil = [
                    dbc.Row([

                        dbc.Col([

                            html.H1('Brasil', className='local-noticias')

                        ]),
                        dbc.Col([]),

                    ]),
                    dbc.Row([

                        dbc.Col([html.Img(id = 'imagem-jornal', style = {'max-width': '50px'})]
                                , style = {'margin-top': '24px'}, md = 1),
                        dbc.Col([html.Div(dcc.Dropdown(lista_jornais_br, value = 'Brazil Journal', id = 'escolher-jornal-br', className = 'dcc-padrao',
                                                        style = {"background-color": 'black', 'color': 'white', 'margin': '12px 0px 0px 0px'}
                                                                 ), style = {'width': "25%"})], style = {'margin-top': '24px'})

                    ]),
                    dbc.Row([

                        html.H1('Finanças', className='classe-noticias')

                    ]),

                    
                    html.Div(id = 'financas-br', style = {'display': 'flex', 'flex-wrap': "wrap", 'gap': '12px'}),

                    
                    dbc.Row([

                        html.H1('Tecnologia', className='classe-noticias')

                    ]),

                    html.Div(id = 'tech-br', style = {'display': 'flex', 'flex-wrap': "wrap", 'gap': '12px'}),
                    
                    ]


layout_mundo = [
                    dbc.Row([

                        dbc.Col([

                            html.H1('Mundo', className='local-noticias')

                        ]),
                        dbc.Col([]),

                    ]),
                    dbc.Row([

                        dbc.Col([html.Img(id = 'imagem-jornal-gringo', style = {'max-width': '50px'})]
                                , style = {'margin-top': '24px'}, md = 2),
                        dbc.Col([html.Div(dcc.Dropdown(lista_jornais_gringos, value = 'Financial Times', id = 'escolher-jornal-gringo', className = 'dcc-padrao',
                                                        style = {"background-color": 'black', 'color': 'white', 'margin': '12px 0px 0px 0px'}
                                                                 ), style = {'width': "25%"})], style = {'margin-top': '24px'})

                    ]),
                    dbc.Row([

                        html.H1('Finanças', className='classe-noticias')

                    ]),

                    
                    html.Div(id = 'financas-gringo', style = {'display': 'flex', 'flex-wrap': "wrap", 'gap': '12px'}),

                    
                    dbc.Row([

                        dbc.Col(html.H1('Tecnologia', className='classe-noticias'), md = 4, style = {'margin-left': '-14px'}),
                        dbc.Col(dcc.RadioItems([' Deep Dive/IA'], id = 'botao-edicao-especial'), style={'display': 'flex', 'justify-content': 'left', 'margin-top': "30px"})

                    ]),

                    html.Div(id = 'tech-gringo', style = {'display': 'flex', 'flex-wrap': "wrap", 'gap': '12px'}),
                    
                    ]

def gerar_tabela_noticias(noticias, jornal, tema):

    noticias['jornal'] = noticias['jornal'].fillna("").str.strip()
    noticias['manchete'] = noticias['manchete'].fillna("").str.strip()
    noticias['topico'] = noticias['topico'].fillna("").str.strip()

    noticias_filtradas = pd.DataFrame()


    if jornal == 'G1':

        noticias = noticias[(noticias['jornal'] == 'g1') & (noticias['topico'] == tema)]
        
    elif jornal == 'Brazil Journal':

    
        noticias_filtradas = noticias[(noticias['jornal'] == 'brazil_journal') & (noticias['topico'] == tema)]

    elif jornal == 'Valor Econômico':
        noticias = noticias[
            (noticias['jornal'] == 'valor_economico') & (noticias['topico'] == tema)]
        
        # Adiciona notícias placeholder caso faltem entradas
    elif noticias_filtradas.empty:
        noticias_filtradas = pd.DataFrame({
            'manchete': ["Nenhuma notícia disponível"] * 6,
            'subtopico': ["-"] * 6,
            'link': ["#"] * 6,
            'topico': ["-"] * 6,
            'jornal': ["brazil_journal"] * 6
        })

    elif jornal == 'WSJ':

        noticias = noticias[(noticias['jornal'] == 'wsj') & (noticias['topico'] == tema)]

        if tema == 'ia':

            noticias_faltantes = pd.DataFrame({'manchete': "-", 'subtopico': "-", 'link': "-", 'topico': "-", 'jornal': "-"}, index = [0])

            noticias = pd.concat([noticias, noticias_faltantes], ignore_index=True)

            

    elif jornal == 'Financial Times':

        noticias = noticias[(noticias['jornal'] == 'ft') & (noticias['topico'] == tema)]

    elif jornal == 'Fortune 500':

        noticias = noticias[(noticias['jornal'] == 'fortune') & (noticias['topico'] == tema)]

    noticias = noticias.fillna("-")

    layout_tabela = [dbc.Row([

                           dbc.Col([
                               
                               html.A(children=[

                                html.P(children=noticias['subtopico'].iloc[0], className='h3-noticias'),
                                html.H3(children=noticias['manchete'].iloc[0], className='manchete')

                            ], href= noticias['link'].iloc[0], target= "_blank", className= 'links-noticias'),


                           ], style={'width': '375px'}),
                           dbc.Col([
                               
                               html.A(children=[

                                html.P(children=noticias['subtopico'].iloc[1], className='h3-noticias'),
                                html.H3(children=noticias['manchete'].iloc[1], className='manchete')

                            ], href= noticias['link'].iloc[1], target= "_blank", className= 'links-noticias'),

                           ], style={'width': '375px'}),
                          
                           ]),

                    dbc.Row([

                           dbc.Col([
                               
                               html.A(children=[

                                html.P(children=noticias['subtopico'].iloc[2], className='h3-noticias'),
                                html.H3(children=noticias['manchete'].iloc[2], className='manchete')

                            ], href= noticias['link'].iloc[2], target= "_blank", className= 'links-noticias'),


                           ], style={'width': '375px'}),
                           dbc.Col([
                               
                               html.A(children=[

                                html.P(children=noticias['subtopico'].iloc[3], className='h3-noticias'),
                                html.H3(children=noticias['manchete'].iloc[3], className='manchete')

                            ], href= noticias['link'].iloc[3], target= "_blank", className= 'links-noticias'),

                           ], style={'width': '375px'}),
                          
                           ]),

                    dbc.Row([

                           dbc.Col([
                               
                               html.A(children=[

                                html.P(children=noticias['subtopico'].iloc[4], className='h3-noticias'),
                                html.H3(children=noticias['manchete'].iloc[4], className='manchete')

                            ], href= noticias['link'].iloc[4], target= "_blank", className= 'links-noticias'),


                           ], style={'width': '375px'}),
                           dbc.Col([
                               
                               html.A(children=[

                                html.P(children=noticias['subtopico'].iloc[5], className='h3-noticias'),
                                html.H3(children=noticias['manchete'].iloc[5], className='manchete')

                            ], href= noticias['link'].iloc[5], target= "_blank", className= 'links-noticias'),

                           ], style={'width': '375px'}),
                          
                           ]),
                        ]

    return layout_tabela

@callback(
    Output('imagem-jornal', 'src'),
    Input('escolher-jornal-br', 'value')
)
def update_options(jornal):

    if jornal == 'G1':

        src = './assets/g1.png'

    elif jornal == 'Brazil Journal':

        src = './assets/bj.png'

    elif jornal == 'Valor Econômico':

        src = './assets/valor.png'

    return src

@callback(
    Output('imagem-jornal-gringo', 'src'),
    Input('escolher-jornal-gringo', 'value')
)
def update_options(jornal):

    if jornal == 'WSJ':

        src = './assets/wsj.png'

    elif jornal == 'Financial Times':

        src = './assets/ft.png'

    elif jornal == 'Fortune 500':

        src = './assets/fortune.png'

    return src


@callback(
    Output('financas-br', 'children'),
    Input('escolher-jornal-br', 'value')
)
def update_options(jornal):
    try:
        noticias = pd.read_csv(diretorio)
        noticias['manchete'] = noticias['manchete'].str.strip()

        layout_tabela = gerar_tabela_noticias(noticias, jornal, 'economia')
    except Exception as e:
        print(f"Erro ao gerar tabela para {jornal}: {e}")
        layout_tabela = html.P("Erro ao carregar notícias.")

    
    return layout_tabela


@callback(
    Output('tech-br', 'children'),
    Input('escolher-jornal-br', 'value')
)
def update_options(jornal):

    try:
        noticias = pd.read_csv(diretorio)
        noticias['manchete'] = noticias['manchete'].str.strip()

        layout_tabela = gerar_tabela_noticias(noticias, jornal, 'tech')
    except Exception as e:
        print(f"Erro ao gerar tabela para {jornal}: {e}")
        layout_tabela = html.P("Erro ao carregar notícias.")

    
    return layout_tabela

@callback(
    Output('financas-gringo', 'children'),
    Input('escolher-jornal-gringo', 'value')
)
def update_options(jornal):

    try:
        noticias = pd.read_csv(diretorio)
        noticias['manchete'] = noticias['manchete'].str.strip()

        layout_tabela = gerar_tabela_noticias(noticias, jornal, 'economia')
    except Exception as e:
        print(f"Erro ao gerar tabela para {jornal}: {e}")
        layout_tabela = html.P("Erro ao carregar notícias.")

    
    return layout_tabela

@callback(
    Output('tech-gringo', 'children'),
    [Input('escolher-jornal-gringo', 'value'),
     Input('botao-edicao-especial', 'value')]
)
def update_options(jornal, botao):

    try:
        noticias = pd.read_csv(diretorio)
        noticias['manchete'] = noticias['manchete'].str.strip()

        if botao == ' Deep Dive/IA':

            if jornal == "Financial Times":

                layout_tabela = gerar_tabela_noticias(noticias, jornal, 'deep_dive')
            
            else:

                layout_tabela = gerar_tabela_noticias(noticias, jornal, 'ia')

        else:

            layout_tabela = gerar_tabela_noticias(noticias, jornal, 'tech')
    except Exception as e:
        print(f"Erro ao gerar tabela para {jornal}: {e}")
        layout_tabela = html.P("Erro ao carregar notícias.")
    
    return layout_tabela













