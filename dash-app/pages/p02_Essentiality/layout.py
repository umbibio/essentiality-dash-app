from dash import Dash, html,dash_table,dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from pages.components.dropdown_selected_gene import dropdown_selected_gene
from pages.components.data_loader import load_data,genome_data,genome
from pages.components.scatter_ploy import scatter_plot,scatter_plot2,scatter_plot3
from pages.components.igv import return_igv
from pages.components.data import table
from pages.components.pileUp import return_pileup
path = r'assets/MIS_OIS_BM.xlsx'



menu = [
     
]

body = [
    html.Br(),
    dbc.Card(
        dbc.CardBody(
            table())
        ),
    html.Br(),
    dcc.Download(id="data-download"),
    dbc.Button("Download Table", id="download-button"),
    html.Br(),
    html.Br(),
    dbc.Card(dcc.Loading(id='igv-container')),
    html.Br(),
   
    dbc.Row([dbc.Col(dbc.Card(scatter_plot())),
    dbc.Col(dbc.Card(scatter_plot2())),
    dbc.Col(dbc.Card(scatter_plot3()))]) 
]
