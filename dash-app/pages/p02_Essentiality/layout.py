from dash import Dash, html,dash_table,dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from pages.components.data_loader import load_data,genome_data,genome
from pages.components.scatter_plot import scatter_plot,scatter_plot2,scatter_plot3


def make_filter_popover(name, data, step):
    return html.Div([
        dbc.Button('Filter', id=f'network-nodes-table-filter-{name}-toggle-button', color='primary', size='sm'),
        dbc.Popover(
            [
                dbc.PopoverBody([
                    dcc.RangeSlider(
                        id=f'{name}-slider',
                        marks={i: str(i) for i in range(int(data['min']), int(data['max']) + 1)},
                        min=0,
                        max=data['max'],
                        step=step,
                        tooltip={'placement': 'bottom', 'always_visible': True},
                        dots=True,
                    )
                ]),
            ],
            id=f'network-nodes-table-filter-{name}-popover',
            target=f'network-nodes-table-filter-{name}-toggle-button',
            trigger='legacy',
            style={'width': '600px'},
        ),
    ])

# Assuming you have data and a step value
data_name = {'No_of_TTAA': {'min': 0, 'max': 180}, 'MIS': {'min': 0, 'max': 1}, 'OIS': {'min': 0, 'max': 1}, 'HMS': {'min': 0, 'max': 1}}
step_value = 0.01

filter_inputs = {
    'GeneIDPkH': dbc.Input(id='network-nodes-table-filter-GeneIDPkH', placeholder='Filter ...', size='sm'),
    'Product_Description': dbc.Input(id='network-nodes-table-filter-Product_Description', placeholder='Filter ...', size='sm'),
    'No_of_TTAA': make_filter_popover('No_of_TTAA', data_name['No_of_TTAA'], 10),
    'MIS': make_filter_popover('MIS', data_name['MIS'], step_value),
    'OIS': make_filter_popover('OIS', data_name['OIS'], step_value),
    'HMS': make_filter_popover('HMS', data_name['HMS'], step_value),
    'GeneIDPf3D7': dbc.Input(id='network-nodes-table-filter-GeneIDPf3D7', placeholder='Filter ...', size='sm'),
    'GeneIDPbANKA': dbc.Input(id='network-nodes-table-filter-GeneIDPbANKA', placeholder='Filter ...', size='sm'),
}

table_columns = [
    {"id": "GeneIDPkH", "name": "GeneID.PkH", "editable": False,'header_style': {'width': '10%', 'minWidth': '120px'}, 'style': {'width': '10%', 'minWidth': '120px'}},
    {"id": "Product_Description", "name": "Product_Description", "editable": False,'header_style': {'width': '10%', 'minWidth': '100px'}, 'style': {'width': '20%', 'minWidth': '120px'}},
    {"id": "No_of_TTAA", "name": "No_of_TTAA", "editable": False,'header_style': {'width': '10%', 'minWidth': '120px'}, 'style': {'width': '10%', 'minWidth': '120px'}},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '5%', 'minWidth': '120px'}, 'style': {'width': '5%', 'minWidth': '120px'}},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '5%', 'minWidth': '120px'}, 'style': {'width': '5%', 'minWidth': '120px'}},
    {"id": "HMS", "name": "HMS", "editable": False,'header_style': {'width': '5%', 'minWidth': '120px'}, 'style': {'width': '5%', 'minWidth': '120px'}},
    {"id": "GeneIDPf3D7", "name": "GeneID.Pf_3D7", "editable": False,'header_style': {'width': '5%', 'minWidth': '120px'}, 'style': {'width': '10%', 'minWidth': '120px'}},
    {"id": "GeneIDPbANKA", "name": "GeneID.Pb_ANKA", "editable": False,'header_style': {'width': '5%', 'minWidth': '120px'}, 'style': {'width': '10%', 'minWidth': '120px'}},
]

menu = []

body = [
      dcc.Store(id='selected-network-nodes', data=[]),
    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.H4('Table for essentiality'),
                html.Small('select or deselect a gene by clicking on a row in the table below'),
            ]),
            dbc.CardBody([
                dbc.Row(dbc.Col(
                    dbc.Table([
                       html.Thead([
                           html.Tr([html.Th(col['name'], style=col['header_style']) for col in table_columns]),
                            html.Tr([html.Th(filter_inputs[col['id']]) for col in table_columns]),
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
    dcc.Download(id="download-data"),
    dbc.Button("Download Table", id="download-button", n_clicks=0),
    html.Br(),
    html.Br(),
    dbc.Card(dcc.Loading(id='igv-container')),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(scatter_plot2())),
    dbc.Col(dbc.Card(scatter_plot())),
    dbc.Col(dbc.Card(scatter_plot3()))]) 
]
