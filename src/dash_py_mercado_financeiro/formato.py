import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, callback
from src.components import ativos_ao_vivo, graficos_ativos, setores, economia, noticias
from src.dash_py_mercado_financeiro.app import *

tab_painel = html.Div([

    dbc.Row(

        [dbc.Col(html.H2(children = "Mercado ao vivo", className='subtitulos-dash'), md = 8),
        dbc.Col(html.H2(children = "Economia", className='subtitulos-dash'), md = 4)]
    ),
    dbc.Row(

        [dbc.Col(
            [
                dbc.Row(ativos_ao_vivo.layout),
                dbc.Row(graficos_ativos.layout),
            ]

        ),
         dbc.Col(setores.layout),
         dbc.Col(economia.layout),]


    ),

])


tab_noticias =  dbc.Row(

    [
        dbc.Col(noticias.layout_brasil, style= {'margin': '24px 0px 0px 150px'}),
        dbc.Col(noticias.layout_mundo, style= {'margin': '24px 0px 0px 0px'})
    ]
)



app.layout = dbc.Container(

    dbc.Row(
        dbc.Col(
            dbc.Tabs([

                dbc.Tab(tab_painel, label = 'Painel'),
                dbc.Tab(tab_noticias, label = 'Notícias')

                      ]), style = {'margin': '8px'}
        )
    ), fluid = True, style = {'height': '100vh', 'width': '100%', 'padding': "25px 25px 0px 25px", 'background-color': '#131516'}
)





if __name__ == "__main__":
    app.run_server(debug = True,
                   host = "0.0.0.0",
                   port = 8051)

    























