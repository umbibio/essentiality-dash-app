from dash import Dash, html,dash_table,dcc, callback
import dash_bio as dashbio
from app import app 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import pages.components.fitness_data_plots as fdata
menu = []

def make_filter_popover(name, data, step):
    return html.Div([
        dbc.Button('Filter', id=f'network-nodes-table-filter-{name}-toggle-button', color='primary', size='sm'),
        dbc.Popover(
            [
                dbc.PopoverBody([
                    dcc.RangeSlider(
                        id=f'{name}-slider',
                        # marks={i: str(i) for i in range(int(data['min']), int(data['max']) + 1)},
                        marks={data['min']: str(data['min']), data['max']: str(data['max'])},
                        min=0,
                        max=data['max'],
                        step=step,
                        tooltip={'placement': 'bottom', 'always_visible': False},
                        dots=False,
                        # included=False, 
                        # pushable=True
                    )
                ]),
            ],
            id=f'network-nodes-table-filter-{name}-popover',
            target=f'network-nodes-table-filter-{name}-toggle-button',
            trigger='legacy',
            style={'width': '600px'},
        ),
    ])

# Define data and step value for filter popovers
data_name = {'MFS.slope': {'min': -2, 'max': 2}, 'lm.p.value': {'min': 0, 'max': 1}, 'lm.adjusted.p.value': {'min': 0, 'max': 1}, 'e.pvalue': {'min': 0, 'max': 1}}
step_value = 0.1

# Define filter inputs for each column
filter_inputs = {
    'geneID': dbc.Input(id='network-nodes-table-filter-GeneID', placeholder='Filter ...', size='sm'),
    'Product.Description': dbc.Input(id='network-nodes-table-filter-Product_Description', placeholder='Filter ...', size='sm'),
    'MFS.slope': make_filter_popover('MFS_slope', data_name['MFS.slope'], 0.001),
    'lm.p.value': make_filter_popover('lm_p_value', data_name['lm.p.value'], step_value),
    'lm.adjusted.p.value': make_filter_popover('lm_adjusted_p_value', data_name['lm.adjusted.p.value'], step_value),
    'e.pvalue': make_filter_popover('e_pvalue', data_name['e.pvalue'], step_value),
}

# Define table columns
table_columns = [
    {"id": "geneID", "name": "GeneID", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
    {"id": "MFS.slope", "name": "FIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "lm.p.value", "name": "lm.p.value", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "lm.adjusted.p.value", "name": "lm.adjusted.p.value", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
     {"id": "Product.Description", "name": "Product_Description", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '15%', }},
    {"id": "e.pvalue", "name": "e.pvalue", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
]

body = [
      dcc.Store(id='selected-network-nodes-ft', data=[]),
      dcc.Store(id='gene-list-store-ft', data={}),
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
                           html.Tr([
                         html.Th(
                                filter_inputs[col['id']]
                            ) for col in table_columns ])


                            ])

                        ],
                    id='network-nodes-table-header-ft',
                    class_name='mb-0'),
                )),
                dbc.Row(dbc.Col(
                    dbc.Spinner([

                    dbc.Table(id='network-nodes-table-ft', hover=True),

                    ], id=f'loading-network-nodes-table-ft', type='border', fullscreen=False, color='primary', delay_hide=0,),
                )),
                dbc.Row([
                    dbc.Col([
                        dbc.Pagination(id='network-nodes-table-pagination-ft', active_page=1, max_value=2, first_last=True, previous_next=True, fully_expanded=False, size='sm', class_name='primary outline'),
                    ], width={'offset': 6, 'size': 4}, ),
                    dbc.Col([
                        html.Div(dbc.RadioItems(
                            id='network-nodes-table-page-size-radio-ft',
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
                        ), className='radio-group-ft'),
                    ], width={'size': 2}, ),
                ]),
              dbc.Row([
        dbc.Col([
            dbc.Modal([
                dbc.ModalHeader("Upload Gene List"),
                dbc.ModalBody([
                    dcc.Markdown("Please upload a .txt or .csv file with comma-separated GeneIds."),
                    dcc.Upload(
                        id='upload-gene-list-ft',
                        children=dbc.Button('Upload Gene List'),
                        multiple=False
                    ),
                    html.Hr(),
                    dcc.Markdown("Or copy and paste the comma seperated gene list below:"),
                    dcc.Textarea(id='copy-paste-gene-list-ft',rows=10, placeholder='Paste GeneIds here'),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Upload", id="upload-modal-button-ft", color="primary"),
                ]),
            ],
                id="upload-modal-ft",
                is_open=False,
            ),
            dbc.Button("Upload gene list", id="open-modal-button-ft"),
        ]),
  
    dbc.Col([
        dbc.Button("Clear gene list", id="clear-button-ft"),
    ])
      ]),

            ]),
        ]),
    ],)], class_name='mb-4'),
     html.Br(),
    dcc.Download(id="download-data-ft"),
    dbc.Button("Download Table", id="download-button-ft",n_clicks=0),
    html.Br(),
    html.Br(),
     dbc.Card( dbc.CardBody([
            dcc.Graph(
                id='scatter-plot-ft',
                figure=fdata.fig,
            ),
            ]),class_name="mb-3",
     ),
     dcc.Store(id='gene-list-store-trending-ft', data=("PKNH_0621300","PKNH_0722900",
              )),
    dbc.Card([
            dbc.CardHeader(html.H4('Trending Plot'),),
            dbc.Row([
            dbc.Row(id='trending-plot-container')]
            ),
            # dbc.Row([ dcc.Graph(
            #     id='trending-plot1',
            #     figure={},
            # ),])
            ]),
]