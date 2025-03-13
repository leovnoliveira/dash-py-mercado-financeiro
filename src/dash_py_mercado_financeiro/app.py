import dash_bootstrap_components as dbc
import logging
import dash
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(BASE_DIR, "logs")


app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY]
)
app.logger.setLevel(logging.DEBUG)