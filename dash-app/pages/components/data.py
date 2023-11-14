from dash import Dash, html,dash_table,dcc, callback
from pages.components.data_loader import load_data

path = r'assets\MIS_OIS_BM.xlsx'
data = load_data(path)

def table():
  return dash_table.DataTable(
                               id ='table',
                               data=data.to_dict('records'), 
                                page_size=10,
                                style_table={
                                'border': '1px solid black',  
                               'borderCollapse': 'collapse', 
                               'borderTop': 'none', 
                               'borderBottom': 'none', 
                                'color': 'black' ,
                               'margin': 'auto'
                                },
                                style_header={'fontWeight': 'bold'},
                                style_cell={'textAlign': 'left', 'fontSize': '16px',
                                'border': '1px solid black',
                                'padding': '5px', 
                                 'color': 'black', 
                               'margin': 'auto' },
                               row_selectable='single',
                               )
