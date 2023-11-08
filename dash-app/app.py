from dash import Dash,html
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc


theme="spacelab"
external_stylesheets = [
    getattr(dbc.themes, theme.upper()),
    dbc.icons.BOOTSTRAP,
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title='DashBoard', update_title='Loading...')

server = app.server