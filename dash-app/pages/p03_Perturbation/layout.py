from dash import dcc, html
import dash_bootstrap_components as dbc
import pages.components.pertutbation_data as pdata

menu = None

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
data_name = {'SetA_GNF_High_day15_logFC': {'min': -10, 'max': 10}, 'SetA_GNF_High_day15_PValue': {'min': 0, 'max': 1}, 'SetA_GNF_High_day15_FDR': {'min': 0, 'max': 1}, 'SetA_GNF_High_day15_mean_FC_sites': {'min': -10, 'max': 10}}
step_value = 0.1

# Define filter inputs for each column                                                                                                                                                                  
#filter_inputs = {
#    'geneID': dbc.Input(id='network-nodes-table-filter-GeneID', placeholder='Filter ...', size='sm'),
#    'Product.Description': dbc.Input(id='network-nodes-table-filter-Product_Description', placeholder='Filter ...', size='sm'),
#    'Symbol': dbc.Input(id='network-nodes-table-filter-symbol', placeholder='Filter ...', size='sm'),
#    'SetA_GNF_High_day15_logFC': make_filter_popover('SetA_GNF_High_day15_logFC', data_name['SetA_GNF_High_day15_logFC'], step_value),
#    'SetA_GNF_High_day15_PValue': make_filter_popover('SetA_GNF_High_day15_PValue', data_name['SetA_GNF_High_day15_PValue'], 0.01),
#    'SetA_GNF_High_day15_FDR': make_filter_popover('SetA_GNF_High_day15_FDR', data_name['SetA_GNF_High_day15_FDR'], step_value),
#    'SetA_GNF_High_day15_mean_FC_sites': make_filter_popover('SetA_GNF_High_day15_mean_FC_sites', data_name['SetA_GNF_High_day15_mean_FC_sites'], step_value),
#    'SetA_GNF_High_day15_cv_inverse': make_filter_popover('SetA_GNF_High_day15_cv_inverse', data_name['SetA_GNF_High_day15_cv_inverse'], 0.01),
#    'SetB_GNF_High_day15_logFC': make_filter_popover('SetB_GNF_High_day15_logFC', data_name['SetB_GNF_High_day15_logFC'], step_value),
#    'SetB_GNF_High_day15_PValue': make_filter_popover('SetB_GNF_High_day15_PValue', data_name['SetB_GNF_High_day15_PValue'], 0.01),
#    'SetB_GNF_High_day15_FDR': make_filter_popover('SetB_GNF_High_day15_FDR', data_name['SetB_GNF_High_day15_FDR'], step_value),
#    'SetB_GNF_High_day15_mean_FC_sites': make_filter_popover('SetB_GNF_High_day15_mean_FC_sites', data_name['SetB_GNF_High_day15_mean_FC_sites'], step_value),
#    'SetB_GNF_High_day15_cv_inverse': make_filter_popover('SetB_GNF_High_day15_cv_inverse', data_name['SetB_GNF_High_day15_cv_inverse'], 0.01),
#}

# Define table columns                                                                                                                                                                                  
table_columns = [
    {"id": "geneID", "name": "GeneID", "editable": False,'header_style': {'width': '15%', }, 'style': {'width': '15%', }},
    {"id": "Product.Description", "name": "Product.Description", "editable": False,'header_style': {'width': '25%', }, 'style': {'width': '25%', }},
    {"id": "Symbol", "name": "Symbol", "editable": False,'header_style': {'width': '15%', }, 'style': {'width': '15%', }},
    {"id": "SetA_GNF_High_day15_logFC", "name": "SetA_day15_log2FC", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetA_GNF_High_day15_PValue", "name": "SetA_day15_PValue", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetA_GNF_High_day15_FDR", "name": "SetA_day15_FDR", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetA_GNF_High_day15_mean_FC_sites", "name": "setA_FC_siteslevel", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetA_GNF_High_day15_cv_inverse", "name": "SetA_day15_CVinverse", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetB_GNF_High_day15_logFC", "name": "SetB_day15_log2FC", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetB_GNF_High_day15_PValue", "name": "SetB_day15_PValue", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetB_GNF_High_day15_FDR", "name": "SetB_day15_FDR", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetB_GNF_High_day15_mean_FC_sites", "name": "setB_FC_siteslevel", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }},
    {"id": "SetB_GNF_High_day15_cv_inverse", "name": "SetB_day15_CVinverse", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '12%', }}        
]

body = [
    dbc.Card(
            # dbc.CardHeader(html.H2("Plasmodium Knowlesi Essentiality Database")),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown('''
After selection of the transposon library with GNF179 and DHA, two statistical models, EdgeR and a ‘site level’ model, were used to identify genes with significantly changed numbers of insertions. 
 CV inverse is a metric to measure whether the increasing or decreasing insertion pattern are evenly distributed across all TTAA sites within the CDS of the gene.                                                               
''')),
])),
     class_name="mb-4 mt-4"),

    ####Add a dbc.Card(box) for header                                                                                                                                        
    #dbc.Card(
    #    dbc.CardBody(dbc.Card(html.H4('GNF179 drug perturbation'))), class_name="rounded-3 mb-4"),
    #####Reorganize


    
    dbc.Card(
          dbc.CardBody([
        dbc.CardHeader(html.H4('GNF179 drug perturbation'), className="rounded-3 mb-4"),
              #######Insert table

              #######Insert table
            dbc.Card([
                dbc.CardHeader(html.H6("You can upload a comma seperated gene list containing at max of 10 genes and view the poisition of them respective to rest and also trending.Those genes being input has no sufficient data such as low TTAA will not be shown in the scatter plots below:")),
        dbc.CardBody([
            dbc.Row([
            dbc.Col([
            dbc.Button("Upload gene list", id="open-modal-button_pr", size="md"),  
            ]),
            html.Br(),  # Add line break
            dbc.Col([
            dbc.Button("Clear gene list", id="clear-button_pr", size="md"),  
            ]),
        ]),
        ]),
    ],className="rounded-3 mb-4 mt-4"
    ),
        dbc.Modal([
        dbc.ModalHeader("Upload Gene List"),
        dbc.ModalBody([
            dcc.Markdown("Please upload a .txt or .csv file with comma-separated GeneIds."),
            dcc.Upload(
                id='upload-gene-list_pr',
                children=dbc.Button('Upload Gene List'),
                multiple=False
            ),
            html.Hr(),
            dcc.Markdown("Or copy and paste the comma-separated gene list below:"),
            dcc.Textarea(id='copy-paste-gene-list_pr', rows=10, placeholder='Paste GeneIds here'),
        ]),
        dbc.ModalFooter([
            dbc.Button("Upload", id="upload-modal-button_pr", color="primary"),
        ]),
    ],
        id="upload-modal_pr",
        is_open=False,
    ),
    dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id='scatter-plot',
                figure=pdata.fig,
            ),
        ]),
        className="rounded-3"  # Add rounded corners to the card
    ),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='scatter-plot1',
                        figure=pdata.fig1,
                    ),
                ]),
                dbc.Col([
                    dcc.Graph(
                        id='scatter-plot2',
                        figure=pdata.fig2,
                    ),
                ])
            ])
        ]),
        className="rounded-3 mt-5"  # Add rounded corners to the card and margin top
    ),
    dcc.Store(id='gene-list-store_pr', data=()),
    dbc.Card( dbc.CardBody([
        dbc.CardHeader(html.H4('Trending Plot',className="rounded-3")),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='trending-plot',
                    figure={},
                ),
            ]),
            dbc.Col([
                dcc.Graph(
                    id='trending-plot1',
                    figure={},
                ),
            ])
        ])
        ]) , className="rounded-3 mt-5"
    ),
    dcc.Download(id="download-data_pr"),
    dbc.Button("Download Data", id="download-button_pr",n_clicks=0,className="mt-3"),
    ]),
        className="rounded-3 mb-4 mt-4"  # Add rounded corners to the card
    ),
    


    dbc.Card(
        dbc.CardBody([
         dbc.CardHeader(html.H4('DHA drug perturbation') ,className="rounded-3 mb-4 "),
             dbc.Card([
                 dbc.CardHeader(html.H6("You can upload a comma seperated gene list containing at max of 10 genes and view the poisition of them respective to rest and also trending.Those genes being input has no sufficient data such as low TTAA will not be shown in the scatter plots below:")),
        dbc.CardBody([
            dbc.Row([
            dbc.Col([
            dbc.Button("Upload gene list", id="open-modal-button_pr_DHA", size="md"),  
            ]),
            html.Br(),  # Add line break
            dbc.Col([
            dbc.Button("Clear gene list", id="clear-button_pr_DHA", size="md"),  
            ]),
        ]),
        ]),
    ],className="rounded-3 mb-4 mt-4"
    ),
    dbc.Modal([
        dbc.ModalHeader("Upload Gene List"),
        dbc.ModalBody([
            dcc.Markdown("Please upload a .txt or .csv file with comma-separated GeneIds."),
            dcc.Upload(
                id='upload-gene-list_pr_DHA',
                children=dbc.Button('Upload Gene List'),
                multiple=False
            ),
            html.Hr(),
            dcc.Markdown("Or copy and paste the comma-separated gene list below:"),
            dcc.Textarea(id='copy-paste-gene-list_pr_DHA', rows=10, placeholder='Paste GeneIds here'),
        ]),
        dbc.ModalFooter([
            dbc.Button("Upload", id="upload-modal-button_pr_DHA", color="primary"),
        ]),
    ],
        id="upload-modal_pr_DHA",
        is_open=False,
    ),
    dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                id='scatter-plot_DHA',
                figure=pdata.fig_DHA,
            ),
        ]),
        className="rounded-3"  # Add rounded corners to the card
    ),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='scatter-plot1_DHA',
                        figure=pdata.fig1_DHA,
                    ),
                ]),
                dbc.Col([
                    dcc.Graph(
                        id='scatter-plot2_DHA',
                        figure=pdata.fig2_DHA,
                    ),
                ])
            ])
        ]),
        className="rounded-3 mt-5"  # Add rounded corners to the card and margin top
    ),
    dcc.Store(id='gene-list-store_pr_DHA', data=()),
    dbc.Card( dbc.CardBody([
        dbc.CardHeader(html.H4('Trending Plot',className="rounded-3")),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='trending-plot_DHA',
                    figure={},
                ),
            ]),
            dbc.Col([
                dcc.Graph(
                    id='trending-plot1_DHA',
                    figure={},
                ),
            ])
        ])
        ]) , className="rounded-3 mt-5"
    ),
    dcc.Download(id="download-data_pr_DHA"),
    dbc.Button("Download Data", id="download-button_pr_DHA",n_clicks=0,className="mt-3"),
    ]),
        className="rounded-3 mb-4 mt-4"  # Add rounded corners to the card
    ),
]
