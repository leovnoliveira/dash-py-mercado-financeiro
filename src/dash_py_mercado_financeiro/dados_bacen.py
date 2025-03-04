import os
from bcb import sgs
from datetime import datetime
from datetime import timedelta
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "data")

def att_inflacao():

    hoje = datetime.now()
    inicio = hoje - timedelta(days = 4000)

    inflacao = None

    while isinstance(inflacao, pd.DataFrame) == False:

        inflacao = sgs.get({'ipca': 433,
                            'igp-m': 189},
                            start= inicio)
        
        inflacao = inflacao/100
        inflacao_csv_path = os.path.join(DATA_DIR, "inflacao.csv")
        inflacao.to_csv(inflacao_csv_path)

def att_divida_pib():

        hoje = datetime.now()
        um_ano_atras = hoje - timedelta(days=4000)

        divida_pib = None

        while isinstance(divida_pib, pd.DataFrame) == False:

            divida_pib = sgs.get({'DIVIDA_PIB': 13762},
                            start= um_ano_atras)
            
        divida_pib = divida_pib/100
        divida_pib_csv_path = os.path.join(DATA_DIR, "divida_pib.csv")
        divida_pib.to_csv(divida_pib_csv_path)
        print(f"Arquivo salvo em {divida_pib_csv_path}")

def att_dolar():

        hoje = datetime.now()
        inicio = hoje - timedelta(days=4000)
        dolar = None

        while isinstance(dolar, pd.DataFrame) == False:

            dolar = sgs.get({'DOLAR': 1},
                            start= inicio)
        
        dolar_csv_path = os.path.join(DATA_DIR, 'dolar.csv')
        dolar.to_csv(dolar_csv_path)

if __name__ == "__main__":

    att_inflacao()
    att_divida_pib()
    att_dolar()