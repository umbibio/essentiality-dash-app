from dash import Dash, html,dash_table,dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from pages.components.dropdown_selected_gene import dropdown_selected_gene
from pages.components.data_loader import load_data,genome_data,genome
from pages.components.scatter_ploy import scatter_plot,scatter_plot2,scatter_plot3
from pages.components.data import table

path = r'assets/MIS_OIS_BM.xlsx'
data = load_data(path)

def make_filter_popover(name, input_component, delay, **kwargs):
    return html.Div([
        dbc.Button('Filter', id=f'network-nodes-table-filter-{name}-toggle-button', color='primary', size='sm'),
        dbc.Popover(
            [
                dbc.PopoverBody([
                    html.P(id=f'network-nodes-table-filter-{name}-form-message'),
                    input_component(id=f'network-nodes-table-filter-{name}', **kwargs),
                ]),
            ],
            id=f'network-nodes-table-filter-{name}-popover',
            target=f'network-nodes-table-filter-{name}-toggle-button',
            trigger='legacy',
            delay={'show': 0, 'hide': 0},
        ),
    ])

filter_inputs = {
    'geneID': dbc.Input(id='network-nodes-table-filter-geneID', placeholder='Filter ...', size='sm'),
    'MIS1': make_filter_popover('MIS1', dcc.RangeSlider, 10000, pushable=True, step=0.01),
    'MIS2': make_filter_popover('MIS2', dcc.RangeSlider, 10000, pushable=True, step=0.01),
    'MIS3': make_filter_popover('MIS3', dcc.RangeSlider, 10000, pushable=True, step=0.01),
    'OIS': make_filter_popover('OIS', dcc.RangeSlider, 10000, pushable=True, step=0.01),
    'BM': dbc.Input(id='network-nodes-table-filter-BM', placeholder='Filter ...', size='sm'),
}


table_columns = [
    {"id": "geneID", "name": "gene ID", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "MIS1", "name": "MIS1", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "MIS2", "name": "MIS2", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "MIS3", "name": "MIS3", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "BM", "name": "BM", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
]

menu = []

body = [
     dcc.Store(id='network-nodes-table-sort-column-values-state', data=[0 for _ in table_columns]),
      dcc.Store(id='selected-network-nodes', data=[]),
    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.H4('Genes in network'),
                html.Small('select or deselect a gene by clicking on a row in the table bellow'),
            ]),
            dbc.CardBody([
                dbc.Row(dbc.Col(
                    dbc.Table([
                        html.Thead([
                            html.Tr([ html.Th([col['name'], ' ',  html.Span([html.I(className="bi bi-sort-alpha-down sort-icon", id={'type': 'network-nodes-table-sort-column-values', 'id': col['id']})]),], style=col['header_style']) for col in table_columns ]),
                            html.Tr([ html.Th(
                                filter_inputs[col['id']]
                            ) for col in table_columns ]),
                        ])
                    ],
                    id='network-nodes-table-header',
                    class_name='mb-0'),
                )),
                dbc.Row(dbc.Col(
                    dbc.Spinner([

                    dbc.Table(id='network-nodes-table', hover=True),

                    ], id=f'loading-network-nodes-table', type='border', fullscreen=False, color='primary', delay_hide=0,),
                )),
                dbc.Row([
                    dbc.Col([
                        dbc.Pagination(id='network-nodes-table-pagination', active_page=1, max_value=2, first_last=True, previous_next=True, fully_expanded=False, size='sm', class_name='primary outline'),
                    ], width={'offset': 6, 'size': 4}, ),
                    dbc.Col([
                        html.Div(dbc.RadioItems(
                            id='network-nodes-table-page-size-radio',
                            class_name="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-sm btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "10", "value": 10},
                                {"label": "20", "value": 20},
                                {"label": "50", "value": 50},
                            ],
                            value=10,
                        ), className='radio-group'),
                    ], width={'size': 2}, ),
                ]),
            ]),
        ]),
    ],)], class_name='mb-4'),
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
