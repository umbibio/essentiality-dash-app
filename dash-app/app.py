from dash import Dash,html
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc

url_base_pathname = '/test/'

theme="spacelab"
external_stylesheets = [
    getattr(dbc.themes, theme.upper()),
    dbc.icons.BOOTSTRAP,
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    url_base_pathname=url_base_pathname,
    suppress_callback_exceptions=True,
    title='DashBoard', update_title='Loading...')

server = app.server