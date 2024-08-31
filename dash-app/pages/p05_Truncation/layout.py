from dash import dcc
from dash import html
from pages.components import truncation_data as td

import dash_bootstrap_components as dbc

# Define a variable 'menu' which is currently set to None
# Define a function to create a filter popover for a specific column
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
data_name = {'cp': {'min': 0, 'max': 1},'MSE': {'min': 0, 'max': 1},'R_i': {'min': 0, 'max': 1},'TTAA': {'min': 0, 'max': 180}, 'MIS': {'min': 0, 'max': 1}, 'OIS': {'min': 0, 'max': 1}, 'HMS': {'min': 0, 'max': 1}}
step_value = 0.1

# Define filter inputs for each column
filter_inputs = {
    'geneID': dbc.Input(id='network-nodes-table-filter-geneID', placeholder='Filter ...', size='sm'),
    'Product_Description': dbc.Input(id='network-nodes-table-filter-Product_Description', placeholder='Filter ...', size='sm'),
    'Symbol': dbc.Input(id='network-nodes-table-filter-symbol', placeholder='Filter ...', size='sm'),
    'cp': make_filter_popover('cp', data_name['cp'], step_value),
    'MSE': make_filter_popover('MSE', data_name['MSE'], step_value),
    'R_i': make_filter_popover('R_i', data_name['R_i'], step_value),
    'TTAA': [
        make_filter_popover('No_of_TTAA', data_name['TTAA'], 1),
        # dbc.Input(id='network-nodes-table-filter-No_of_TTAA', placeholder='Filter ...',  size='sm', style={'width': '50px'})
    ],
    'MIS': make_filter_popover('MIS', data_name['MIS'], step_value),
    'OIS': make_filter_popover('OIS', data_name['OIS'], step_value),
    'HMS': make_filter_popover('HMS', data_name['HMS'], step_value),
    'Truncation_type': dbc.Input(id='network-nodes-table-filter-Truncation_type', placeholder='Filter ...', size='sm'),
    'MSE_cutoff': dbc.Input(id='network-nodes-table-filter-MSE_cutoff', placeholder='Filter ...', size='sm'),
}

# Define table columns
table_columns = [
    {"id": "geneID", "name": "GeneID", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "Product_Description", "name": "Product.Description", "editable": False,'header_style': {'width': '16%', }, 'style': {'width': '16%', }},
    {"id": "Symbol", "name": "Symbol", "editable": False,'header_style': {'width': '7%', }, 'style': {'width': '7%', }},
    {"id": "cp", "name": "cp", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "MSE", "name": "MSE", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "R_i", "name": "R_i", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
     {"id": "TTAA", "name": "TTAA", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "HMS", "name": "HMS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "Truncation_type", "name": "Truncation_type", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "MSE_cutoff", "name": "MSE_cutoff", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
]

menu = []
# Define the layout of the body using Dash Bootstrap Components
body = [     dbc.Card(
            # dbc.CardHeader(html.H2("Plasmodium Knowlesi Essentiality Database")),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown('''
This page is to explore the truncatable genes in P.knowlesi. The raw reads of insertional transposon could be visualized in the IGV window of “essentiality page”.                                                         

''')),
])),
     class_name="mb-4 mt-4"),
    dcc.Store(id='selected-network-nodes-trunc', data=[]),
      dcc.Store(id='gene-list-store-trunc', data={}),
    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.H6('To select or deselect a gene by clicking on a row in the table below'),html.Small(dcc.Markdown('''                                           
- “GeneID”: The unique PlasmoDB gene identifier.                                                 
- “Product.Description”: PlasmoDB gene product description corresponding to the gene accession.                                                  
- “Symbol”: Gene name or symbol from PlasmoDB.                                                
- "cp": The changing points location calculated by the order of the changing point where it has lowest MSE for fitted step function divided by the total number of TTAA within the CDS of the gene. 
- "MSE": The minimum Mean Squared Error value calculated in truncation model of the gene in the truncation changing points in order to measure the goodness of fit, the smaller, the better of the fit.                                                                                                                                     
- "R_i": The relative distance of the changing point's TTAA site to TSS of the gene(The introns of the gene has been removed and all exons are stitched and normalized as 1).
- "TTAA": Total number of TTAA within the CDS of the gene.                                                                                        
- “MIS”: Scores calculated by Mutagenesis Index Score model.                                                 
- “OIS”: Scores calculated by Occupancy Index Score model.                                                  
- “HMS”: Scores calculated by Hybrid Model Score based on BMS(Bayesian network Model score)and MMIS(Modified Mutagenesis Index Score).               
- "Truncation_type": The types of truncations.                                                
- "MSE_cutoff": 25 percentile is stringent cutoff while 75 percentile is moderate cutoff.                                         
''')),
            ]),
            dbc.CardBody([
                dbc.Row(dbc.Col(
                    dbc.Table([
                       html.Thead( children=[
                           html.Tr([html.Th(col['name'], style=col['header_style']) for col in table_columns]),
                           html.Tr([
                         html.Th(
                                filter_inputs[col['id']]
                            ) for col in table_columns ])


                            ])

                        ],
                    id='network-nodes-table-header-trunc',
                     style={'tableLayout': 'fixed', 'width': '100%','fontSize': 'small'},
                    # responsive=True,
                    class_name='mb-0'),
                )),
                dbc.Row(dbc.Col(
                    dbc.Spinner([

                    dbc.Table(id='network-nodes-table-trunc', hover=True,responsive=True,style={'tableLayout': 'fixed', 'width': '100%' , 'fontSize': 'small'} ,),

                    ], id=f'loading-network-nodes-table-trunc', type='border', fullscreen=False, color='primary', delay_hide=0, ),
                )),
                dbc.Row([
                    dbc.Col([
                        dbc.Pagination(id='network-nodes-table-pagination-trunc', active_page=1, max_value=2, first_last=True, previous_next=True, fully_expanded=False, size='sm', class_name='primary outline'),
                    ], width={'offset' : 6 ,'size': 4}),
                    dbc.Col([
                        html.Div(dbc.RadioItems(
                            id='network-nodes-table-page-size-radio-trunc',
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
              dbc.Row([
        dbc.Col([
            dbc.Modal([
                dbc.ModalHeader("Upload Gene List"),
                dbc.ModalBody([
                    dcc.Markdown("Please upload a .txt or .csv file with comma-separated GeneIds."),
                    dcc.Upload(
                        id='upload-gene-list-trunc',
                        children=dbc.Button('Upload Gene List'),
                        multiple=False
                    ),
                    html.Hr(),
                    dcc.Markdown("Or copy and paste the comma seperated gene list below:"),
                    dcc.Textarea(id='copy-paste-gene-list-trunc',rows=10, placeholder='Paste GeneIds here'),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Upload", id="upload-modal-button-trunc", color="primary"),
                ]),
            ],
                id="upload-modal-trunc",
                is_open=False,
            ),
            dbc.Button("Upload gene list", id="open-modal-button-trunc"),
        ]),
  
    dbc.Col([
        dbc.Button("Clear gene list", id="clear-button-trunc"),
    ])
      ]),

            ]),
        ]),
    ],)], class_name='mb-4'),
     html.Br(),
    dcc.Download(id="download-data-trunc"),
    dbc.Button("Download Table", id="download-button-trunc",n_clicks=0),
    html.Br(),
        html.Br(),

    dbc.Row([
        dbc.Col(
             dbc.Card(
        dbc.CardBody([
               dbc.CardHeader(html.H6(" 3' truncation",style={
                        'font-weight': 'bold',  # Makes the text bold
                        'text-align': 'center'  # Centers the text
                    }),className="rounded-3"),
                dcc.Graph(
                id='scatter-plot-trunc',
                figure=td.fig,
            ),
            
        ])
    ),
      class_name="mb-3 2"  ),
        dbc.Col(
             dbc.Card(
        dbc.CardBody([
            dbc.CardHeader(html.H6(" 5' truncation" ,style={
                        'font-weight': 'bold',  # Makes the text bold
                        'text-align': 'center'  # Centers the text
                    }),className="rounded-3"),
                dcc.Graph(
                id='scatter-plot-trunc_5p',
                figure=td.fig,
            ),
            
        ])
    ),
      class_name="mb-3 2"  )
    ],class_name="mb-3" ),
       
           dbc.Row([
        dbc.Col(
             dbc.Card(
        dbc.CardBody([
               dbc.CardHeader(html.H6(" 3' truncation",style={
                        'font-weight': 'bold',  # Makes the text bold
                        'text-align': 'center'  # Centers the text
                    }),className="rounded-3"),
                dcc.Graph(
                id='scatter-plot-trunc_HMS',
                figure=td.fig,
            ),
            
        ])
    ),
      class_name="mb-3 2"  ),
        dbc.Col(
             dbc.Card(
        dbc.CardBody([
            dbc.CardHeader(html.H6(" 5' truncation" ,style={
                        'font-weight': 'bold',  # Makes the text bold
                        'text-align': 'center'  # Centers the text
                    }),className="rounded-3"),
                dcc.Graph(
                id='scatter-plot-trunc_5p_HMS',
                figure=td.fig,
            ),
            
        ])
    ),
      class_name="mb-3 2"  )
    ],class_name="mb-3" ),
            ]




