from dash import Dash,html
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

url_base_pathname = '/PkEssenDB/'

theme="spacelab"
external_stylesheets = [
    getattr(dbc.themes, theme.upper()),
    dbc.icons.BOOTSTRAP,
]
load_figure_template(theme)
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    url_base_pathname=url_base_pathname,
    suppress_callback_exceptions=True,
    title='Plasmodium Essentiality Database', update_title='Loading...')

server = app.server
