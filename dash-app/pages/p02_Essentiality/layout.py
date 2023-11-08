from dash import Dash, html,dash_table,dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from pages.components.dropdown_selected_gene import dropdown_selected_gene
from pages.components.data_loader import load_data
from pages.components.scatter_ploy import scatter_plot,scatter_plot2,scatter_plot3
from pages.components.igv import return_igv
from pages.components.data import table
from pages.components.pileUp import return_pileup
path = r'assets/MIS_OIS_BM.xlsx'
# path_bed = 'D:\\Demo_App\\dash-app\\assets\\Pk_5502transcript.bed'
menu = [
     
    
]

body = [
    
   html.Div(return_igv()),
    dbc.Label([  "Select Gene:"],style={'color': 'Brown','font-family': 'Arial, sans-serif'}),
    dropdown_selected_gene(load_data(path)),
    html.Br(),
    table(),
    dbc.Row([dbc.Col(dbc.Card(scatter_plot())),
    dbc.Col(dbc.Card(scatter_plot2())),
    dbc.Col(dbc.Card(scatter_plot3()))]) 
]
