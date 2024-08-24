from dash import Dash, html,dash_table,dcc, callback
import dash_bio as dashbio
from app import app 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
from pages.components.data_loader import load_data,genome_data,genome
from pages.components.scatter_plot import scatter_plot,scatter_plot2,scatter_plot3

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
data_name = {'No_of_TTAA': {'min': 0, 'max': 180}, 'MIS': {'min': 0, 'max': 1}, 'OIS': {'min': 0, 'max': 1}, 'HMS': {'min': 0, 'max': 1}}
step_value = 0.1

# Define filter inputs for each column
filter_inputs = {
    'GeneIDPkH': dbc.Input(id='network-nodes-table-filter-GeneIDPkH', placeholder='Filter ...', size='sm'),
    'Product_Description': dbc.Input(id='network-nodes-table-filter-Product_Description', placeholder='Filter ...', size='sm'),
    'Symbol': dbc.Input(id='network-nodes-table-filter-symbol', placeholder='Filter ...', size='sm'),
    'No_of_TTAA': [
        make_filter_popover('No_of_TTAA', data_name['No_of_TTAA'], 1),
        # dbc.Input(id='network-nodes-table-filter-No_of_TTAA', placeholder='Filter ...',  size='sm', style={'width': '50px'})
    ],
    'ref_gene_id': dbc.Input(id='network-nodes-table-filter-ref_gene_id', placeholder='Filter ...', size='sm'),
    'class_code': dbc.Input(id='network-nodes-table-filter-class_code', placeholder='Filter ...', size='sm'),
    'MIS': make_filter_popover('MIS', data_name['MIS'], step_value),
    'OIS': make_filter_popover('OIS', data_name['OIS'], step_value),
    'HMS': make_filter_popover('HMS', data_name['HMS'], step_value),
    'GeneIDPf3D7': dbc.Input(id='network-nodes-table-filter-GeneIDPf3D7', placeholder='Filter ...', size='sm'),
    'GeneIDPbANKA': dbc.Input(id='network-nodes-table-filter-GeneIDPbANKA', placeholder='Filter ...', size='sm'),
}

# Define table columns
table_columns = [
    {"id": "GeneIDPkH", "name": "GeneID", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "Product_Description", "name": "Product.Description", "editable": False,'header_style': {'width': '16%', }, 'style': {'width': '16%', }},
    {"id": "Symbol", "name": "Symbol", "editable": False,'header_style': {'width': '7%', }, 'style': {'width': '7%', }},
    {"id": "No_of_TTAA", "name": "TTAA", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "ref_gene_id", "name": "ref_gene_id", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "class_code", "name": "lncRNA_class", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "HMS", "name": "HMS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "GeneIDPf3D7", "name": "GeneIDPf3D7", "editable": False,'header_style': {'width': '11%', }, 'style': {'width': '11%', }},
    {"id": "GeneIDPbANKA", "name": "GeneIDPbANKA", "editable": False,'header_style': {'width': '13%', }, 'style': {'width': '13%', }},
]
# Define the path for the BED file
path_bed = r'assets/Pk_5502transcript_864lncRNAtranscript_modified.bed'
# Load data and create genome information
gene_to_genome = genome_data(path_bed)
genome_list = genome(gene_to_genome)
# Define tracks for IGV component
tracks =[
                {
                    'name': 'TTAA Track',
                    'url': app.get_asset_url('75Pk_20231022_TTAA.sorted.bam'),
                    'indexURL': app.get_asset_url('75Pk_20231022_TTAA.sorted.bai'),
                    'displayMode': 'EXPANDED',
                    'nameField': 'gene',
                    'height': 150,
                    'color': 'rgb(169,169,169)'
                },
                {
                    'name': 'Coding Genes',
                    'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(0,0,255)'
                },
                {
                    'name': 'lncRNA',
                    'url': app.get_asset_url('PkH_RABT_guided_864lncRNA_2.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(0,100,0)'
                },
                {
                    'name': 'TTAA Genome Pos',
                    'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
                    'displayMode': 'COLLAPSED',
                    'height': 100,
                    'color': 'rgb(255,0,0)'
                },
            ]

# Initialize menu as an empty list
menu = []
# Define the layout for the body of the app
body = [
      dcc.Store(id='selected-network-nodes', data=[]),
      dcc.Store(id='gene-list-store', data={}),
    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.H4('Table for essentiality of protein-coding genes and lncRNAs'),
                html.H6('select or deselect a gene or lncRNA by clicking on a row in the table below'),
                # html.Br,
                html.H6('Annotations for table column names:'), html.Small(dcc.Markdown('''                                             
- “GeneID”: The unique PlasmoDB gene identifier.                                                 
- “Product.Description”: PlasmoDB gene product description corresponding to the gene accession.                                                  
- “Symbol”: Gene name or symbol from PlasmoDB.                                                
- “TTAA”: The total number of TTAA within the CDS of the gene.                                                  
- “MIS”: Scores calculated by Mutagenesis Index Score model.                                                 
- “OIS”: Scores calculated by Occupancy Index Score model.                                                  
- “HMS”: Scores calculated by Hybrid model score based on BMS and MMIS.                                                  
- “ref_gene_id”: The gene ID of protein coding genes overlapped                                                 
- “lncRNA_class”: The types of lncRNA.                                                  
- "GeneIDPf3D7": orthologous gene ID for Plasmodium falciparum 3D7                                                  
- "GeneIDPbANKA": orthologous gene ID for Plasmodium berghei ANKA''')),
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
                    id='network-nodes-table-header',
                     style={'tableLayout': 'fixed', 'width': '100%','fontSize': 'small'},
                    # responsive=True,
                    class_name='mb-0'),
                )),
                dbc.Row(dbc.Col(
                    dbc.Spinner([

                    dbc.Table(id='network-nodes-table', hover=True,responsive=True,style={'tableLayout': 'fixed', 'width': '100%' , 'fontSize': 'small'} ,),

                    ], id=f'loading-network-nodes-table', type='border', fullscreen=False, color='primary', delay_hide=0, ),
                )),
                dbc.Row([
                    dbc.Col([
                        dbc.Pagination(id='network-nodes-table-pagination', active_page=1, max_value=2, first_last=True, previous_next=True, fully_expanded=False, size='sm', class_name='primary outline'),
                    ], width={'offset' : 6 ,'size': 4}),
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
              dbc.Row([
        dbc.Col([
            dbc.Modal([
                dbc.ModalHeader("Upload Gene List"),
                dbc.ModalBody([
                    dcc.Markdown("Please upload a .txt or .csv file with comma-separated GeneIds."),
                    dcc.Upload(
                        id='upload-gene-list',
                        children=dbc.Button('Upload Gene List'),
                        multiple=False
                    ),
                    html.Hr(),
                    dcc.Markdown("Or copy and paste the comma seperated gene list below:"),
                    dcc.Textarea(id='copy-paste-gene-list',rows=10, placeholder='Paste GeneIds here'),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Upload", id="upload-modal-button", color="primary"),
                ]),
            ],
                id="upload-modal",
                is_open=False,
            ),
            dbc.Button("Upload gene list", id="open-modal-button"),
        ]),
  
    dbc.Col([
        dbc.Button("Clear gene list", id="clear-button"),
    ])
      ]),

            ]),
        ]),
    ],)], class_name='mb-4'),
     html.Br(),
    dcc.Download(id="download-data"),
    dbc.Button("Download Table", id="download-button",n_clicks=0),
    html.Br(),
    html.Br(),
    # dbc.Card(dcc.Loading(id='igv-container')),
      dbc.Card( dbc.CardBody(
        id='igv-container',
        children=[
            dashbio.Igv(
                reference={
                    'id': "Id",
                    'name': "PKHN",
                    'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
                    'indexURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
                    'order': 1000000,
                    'tracks': tracks
                }
            )
        ] ,
      ) ,class_name="mb-3",
    ),
    html.Br(),
        dbc.Row([dbc.Col(dbc.Card(scatter_plot2()),class_name="mb-3"),
    dbc.Col(dbc.Card(scatter_plot()),class_name="mb-3",),
    dbc.Col(dbc.Card(scatter_plot3())),],class_name="mb-3",) 
]
