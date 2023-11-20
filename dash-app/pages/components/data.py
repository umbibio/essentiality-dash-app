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
                                'border': 'none',
                                'borderCollapse': 'collapse',
                               'margin': 'auto'
                               },
                                style_header={'fontWeight': 'bold','border': 'none'},
                               style_cell={
                                'textAlign': 'left',
                                'fontSize': '16px',
                                'border': 'none',
                                'padding': '5px',
                                'margin': 'auto',
                               'lineHeight': '1.5'  
                               },
                               row_selectable='single',
)
