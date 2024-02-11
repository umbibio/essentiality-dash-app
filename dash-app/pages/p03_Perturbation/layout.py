from dash import dcc
from dash import html

import dash_bootstrap_components as dbc
import pages.components.pertutbation_data  as pdata
menu = None

body = [
        dbc.Card([
            dcc.Graph(
                id='scatter-plot',
                figure=pdata.fig,
            ),
            ]),
        dbc.Card(dbc.Row([
            dbc.Col([ dcc.Graph(
                id='scatter-plot1',
                figure=pdata.fig1,
            ),]),
            dbc.Col([ dcc.Graph(
                id='scatter-plot2',
                figure=pdata.fig2,
            ),])
            ])),
    dcc.Store(id='gene-list-store_pr', data=("PKNH_0621300","PKNH_0722900",
              )),
        dbc.Card([
            dbc.CardHeader(html.H4('Trending Plot'),),
            dbc.Row([
            dbc.Row([ dcc.Graph(
                id='trending-plot',
                figure={},
            ),]),
            dbc.Row([ dcc.Graph(
                id='trending-plot1',
                figure={},
            ),])
            ])]),
            dbc.Card([dbc.Modal([
                dbc.ModalHeader("Upload Gene List"),
                dbc.ModalBody([
                    dcc.Markdown("Please upload a .txt or .csv file with comma-separated GeneIds."),
                    dcc.Upload(
                        id='upload-gene-list_pr',
                        children=dbc.Button('Upload Gene List'),
                        multiple=False
                    ),
                    html.Hr(),
                    dcc.Markdown("Or copy and paste the comma seperated gene list below:"),
                    dcc.Textarea(id='copy-paste-gene-list_pr',rows=10, placeholder='Paste GeneIds here'),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Upload", id="upload-modal-button_pr", color="primary"),
                ]),
            ],
                id="upload-modal_pr",
                is_open=False,
            ),
            dbc.Button("Upload gene list", id="open-modal-button_pr"),
        ]),
  
    dbc.Col([
        dbc.Button("Clear gene list", id="clear-button_pr"),
    ]),
]
