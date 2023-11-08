from dash import Dash,dcc
import dash_bootstrap_components as dbc


menu = None

body = [
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown(),
                    width={'size': '12', 'offset': '0'}),
                ])
            ),
        ], color="light", outline=True),
    ), class_name="mb-4 mt-4"),
]