from dash import dcc, html
import dash_bootstrap_components as dbc
import pages.components.pertutbation_data as pdata

menu = None

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
    dbc.Card(
          dbc.CardBody([
        dbc.CardHeader(html.H4('GNF179 drug perturbation'), className="rounded-3 mb-4"),
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
    dcc.Store(id='gene-list-store_pr', data=("PKNH_0621300", "PKNH_0722900")),
    dbc.Card( dbc.CardBody([
        dbc.CardHeader(html.H4('Trending Plot')),
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
    dbc.Card([
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
    ],
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
    ]),
        className="rounded-3 mb-4 mt-4"  # Add rounded corners to the card
    ),
    


    dbc.Card(
        dbc.CardBody([
         dbc.CardHeader(html.H4('DHA drug perturbation') ,className="rounded-3 mb-4 "),
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
    dcc.Store(id='gene-list-store_pr_DHA', data=("PKNH_0621300", "PKNH_0722900")),
    dbc.Card( dbc.CardBody([
        dbc.CardHeader(html.H4('Trending Plot')),
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
    dbc.Card([
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
    ],
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
    ]),
        className="rounded-3 mb-4 mt-4"  # Add rounded corners to the card
    ),
]