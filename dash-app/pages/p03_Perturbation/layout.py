from dash import dcc
from dash import html

import dash_bootstrap_components as dbc
import pages.components.pertutbation_data  as pdata
menu = None

body = [
        dbc.Card([
            dcc.Graph(
                id='scatter-plot',
                # figure=pdata.p,
            ),
            ]),
        dbc.Card([
            ]),
        dbc.Card([
            ]),
]