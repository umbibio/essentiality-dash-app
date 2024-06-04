from dash import Dash,html
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# Define the base URL pathname for the app
url_base_pathname = '/PkEssenDB/'

# Define the theme for the app
theme="spacelab"

# Define external stylesheets using the Bootstrap theme and icons
external_stylesheets = [
    getattr(dbc.themes, theme.upper()),
    dbc.icons.BOOTSTRAP,
]
# Load the figure template for the specified theme
load_figure_template(theme)

# Create a Dash app instance
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    url_base_pathname=url_base_pathname,
    suppress_callback_exceptions=True,
    title='Plasmodium Knowlesi Essentiality Database', update_title='Loading...')

# Access the underlying Flask server instance , used for deployment
server = app.server
