from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from dash import callback_context 
from pages.components.data_loader import load_data,genome_data,genome
from app import app 
import pandas as pd
import os
import base64
import io
import numpy as np
import json
from dash.exceptions import PreventUpdate

# Set color variables for highlighting in the app
highlight_color = 'green'
grey_color = 'lightgrey'
# Define file paths for different data sets
path_mis = 'assets/MIS_sorted.xlsx'
path_ois = 'assets/OIS_sorted.xlsx'
path_hms = 'assets/HMS_sorted.xlsx'
path= 'assets/MIS_OIS_HMS_Pk_Pf_Pb_table_V3_OISMMISlike_rounded.xlsx'
# Define the path for genome data in BED format
path_bed = r'assets/Pk_5502transcript_864lncRNAtranscript_modified.bed'
# Load genome data from the BED file
gene_to_genome = genome_data(path_bed)
# Extract genome names from the loaded genome data
genome_list = genome(gene_to_genome)
 
 # Load data from Excel files into Pandas DataFrames
df_MIS = load_data(path_mis)
df_MIS['MIS']=df_MIS['MIS'].round(3)
df_OIS = load_data(path_ois)
df_OIS['OIS']=df_OIS['OIS'].round(3)
df_HMS = load_data(path_hms)
df_HMS['HMS']=df_HMS['HMS'].round(3)
data = load_data(path)
columns_to_round = ['HMS', 'MIS', 'OIS']
data[columns_to_round] = data[columns_to_round].round(3)

# Define tracks for visualization in the IGV component
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

# Define columns for the data table
table_columns = [
    {"id": "GeneIDPkH", "name": "GeneID.PkH", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
    {"id": "Product_Description", "name": "Product_Description", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '15%', }},
    {"id": "No_of_TTAA", "name": "No_of_TTAA", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "ref_gene_id", "name": "lncRNA_refgene", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
    {"id": "class_code", "name": "lncRNA_class", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "HMS", "name": "HMS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "GeneIDPf3D7", "name": "GeneID.Pf_3D7", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
    {"id": "GeneIDPbANKA", "name": "GeneID.Pb_ANKA", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '10%', }},
]
# Define the Dash app callback context
ctx = callback_context
# Define the callback for updating selected network nodes
@app.callback(
    Output('selected-network-nodes', 'data'),
    Input({'type': 'net-node-table-tr', 'index': ALL}, 'n_clicks'),
    Input('network-nodes-table', 'children'),
    Input('selected-network-nodes', 'data'),
)
def update_selected_rows(row_n_clicks, table,data):
    """
    Callback to update the list of selected network nodes.

    Parameters:
        - row_n_clicks: Number of clicks on network node rows.
        - table: The children of the network nodes table.
        - data: Currently selected network nodes.

    Returns:
        List: Updated list of selected network nodes.
    """
    if ctx.triggered[0]['prop_id'] == '.':
        raise PreventUpdate
    index = None 
    if len(ctx.triggered) == 1:
        id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        id = json.loads(id_str)
        index = id['index']
    if index is not None:
        if index not in data:
            data = [index]
        else:
            data.remove(index)
    return data

# Define the callback for updating network nodes table and pagination
@app.callback(
    Output('network-nodes-table', 'children'),
    Output('network-nodes-table-pagination', 'max_value'),
    Input('network-nodes-table-pagination', 'active_page'),
    Input('network-nodes-table-page-size-radio', 'value'),
    Input('network-nodes-table-filter-GeneIDPkH', 'value'),
    Input('gene-list-store','data'),
    Input('upload-modal-button', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-GeneIDPf3D7', 'value'),
    Input('network-nodes-table-filter-GeneIDPbANKA', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    # Input('network-nodes-table-filter-No_of_TTAA','value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes', 'data'),
    Input('clear-button', 'n_clicks'), 
    Input('network-nodes-table-filter-ref_gene_id', 'value'),
    Input('network-nodes-table-filter-class_code', 'value'),
)
def update_info_tables(page, page_size, geneid_filter1,list,upload_clicks,description_filter, geneid_filter2, geneid_filter3,TTAA_filter_slider, mis_filter, ois_filter, bm_filter, selected_nodes,clear_clicks,gene_ref_id_filter,class_code_filter):
    """
    Callback to update the network nodes table and pagination.

    Parameters:
        - page: Active page number.
        - page_size: Number of rows per page.
        - geneid_filter1: Gene ID filter for the first coloumn.
        - list: List of gene IDs for filtering.
        - upload_clicks: Number of clicks on the upload button.
        - description_filter: Product description filter.
        - geneid_filter2: Gene ID filter for the 9th coloumn.
        - geneid_filter3: Gene ID filter for the 10th coloumn.
        - TTAA_filter_slider: Range filter for the number of TTAA.
        - mis_filter: Range filter for MIS values.
        - ois_filter: Range filter for OIS values.
        - bm_filter: Range filter for HMS values.
        - selected_nodes: Currently selected network nodes.
        - clear_clicks: Number of clicks on the clear button.
        - ref_gene_id_filter: filter for 4th coloumn.
        - class_code_filter: filter for 5th coloumn.

    Returns:
        Tuple: Updated network nodes table and maximum pagination value.
    """
    page = int(page) - 1

    
    df = data.copy()  # Create a copy to avoid modifying the original data
    if clear_clicks:
        df = data.copy()
    if geneid_filter1 or upload_clicks and not clear_clicks:
        if geneid_filter1 :
           df = df.loc[df['GeneIDPkH'].str.lower().str.contains(geneid_filter1.lower())]
        if upload_clicks:
         gene_ids_list = list.split(',')
         df = df.loc[df['GeneIDPkH'].str.lower().isin([gene_id.lower() for gene_id in gene_ids_list])]
    if description_filter:
     df = df.loc[df['Product_Description'].str.lower().str.contains(description_filter.lower())]
    if TTAA_filter_slider :
     if TTAA_filter_slider :
      df = df.loc[(df['No_of_TTAA'] >= TTAA_filter_slider[0]) & (df['No_of_TTAA'] <= TTAA_filter_slider[1])]
    #  elif TTAA_filter_box:
    #     TTAA_filter = float(TTAA_filter_box) if TTAA_filter_box else 0
        # df = df.loc[df['No_of_TTAA'].astype(float) == TTAA_filter]
    if mis_filter:
      df = df.loc[(df['MIS'] >= mis_filter[0]) & (df['MIS'] <= mis_filter[1])]
    if ois_filter:
     df = df.loc[(df['OIS'] >= ois_filter[0]) & (df['OIS'] <= ois_filter[1])]
    if bm_filter:
     df = df.loc[(df['HMS'] >= bm_filter[0]) & (df['HMS'] <= bm_filter[1])]
    if geneid_filter2:
      df = df.loc[df['GeneIDPf3D7'].str.lower().str.contains(geneid_filter2.lower(),na=False)]
    if geneid_filter3:
     df = df.loc[df['GeneIDPbANKA'].str.lower().str.contains(geneid_filter3.lower(),na=False)]
    if gene_ref_id_filter:
     df = df.loc[df['ref_gene_id'].str.lower().str.contains(gene_ref_id_filter.lower(),na=False)]
    if class_code_filter:
     df = df.loc[df['class_code'].str.lower().str.contains(class_code_filter.lower(),na=False)]


    data_slice = [{'index': i, 'GeneIDPkH': '', 'Product_Description': ''} for i in range(page * page_size, (page + 1) * page_size)]
    for i, item in enumerate(df.iloc[page * page_size:(page + 1) * page_size].to_dict('records')):
        item_with_index = {'index': i, **item}
        data_slice[i].update(item_with_index)

    net_body = [
        html.Tbody([
            html.Tr([
                html.Td(item_with_index.get(c['id'], '-'), style=c['style'])
                for c in table_columns],
                id={'type': 'net-node-table-tr', 'index': item_with_index['index']},
                style={"fontWeight": 'bold'} if item_with_index['index'] in selected_nodes else {
                    "fontWeight": 'normal'},
                className='table-active' if item_with_index['index'] in selected_nodes else '', )
            for item_with_index in data_slice
        ])
    ]

    filtered_data_nrows = len(df)

    return net_body, int(np.ceil(filtered_data_nrows / page_size))




@app.callback(
    Output({'type': 'net-node-table-tr', 'index': MATCH}, 'style'),
    Output({'type': 'net-node-table-tr', 'index': MATCH}, 'className'),
    State({'type': 'net-node-table-tr', 'index': MATCH}, 'id'),
    Input('selected-network-nodes', 'data'), )
def update_selected_rows_style(id, data):
    """
    Callback to update the style of selected rows in the network nodes table.

    Parameters:
        - id: Identifier of the selected row.
        - data: Currently selected network nodes.

    Returns:
        Tuple: Style and class name for the selected row.
    """
    if id['index'] in data:
        style = {"fontWeight": 'bold'}
        className = 'table-active'
    else:
        style = {"fontWeight": 'normal'}
        className = ''
    return style,className


@app.callback(
    Output('igv-container', 'children'),
    Input('network-nodes-table', 'children'),
    Input('selected-network-nodes', 'data'),
)
def update_igv_locus(table, selected_cells): 
    """
    Callback to update the IGV container based on selected network nodes.

    Parameters:
        - table: The children of the network nodes table.
        - selected_cells: Currently selected network nodes.

    Returns:
        List: Updated IGV container children.
    """
    trigger_id = ctx.triggered_id.split('.')[0]
    if trigger_id == 'network-nodes-table':
        raise PreventUpdate
    elif selected_cells:
        selected_index = selected_cells[0]
        row = table[0]['props']['children'][selected_index]['props']['children']
        gene = row[0]
        gene_name = gene['props']['children']
        genome_name = gene_to_genome.get(gene_name)
        return [
            dashbio.Igv(
                locus=genome_name,
                reference={
                    'id': "Id",
                    'name': "PKHN",
                    'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
                    'indexURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
                    'order': 1000000,
                    'tracks': tracks
                }
            )
        ]
    else :
        return [
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
        ]

    




@app.callback(
    Output('download-button', 'n_clicks'),
    Input('network-nodes-table-filter-GeneIDPkH', 'value'),
    Input('gene-list-store','data'),
   Input('upload-modal-button', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-GeneIDPf3D7', 'value'),
    Input('network-nodes-table-filter-GeneIDPbANKA', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    # Input('network-nodes-table-filter-No_of_TTAA','value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes', 'data'),
    Input('clear-button', 'n_clicks'), 
    Input('network-nodes-table-filter-ref_gene_id', 'value'),
    Input('network-nodes-table-filter-class_code', 'value'),

    prevent_initial_call=True,
) 
def reset_n_clicks(geneid_filter1,list,upload_clicks,description_filter, geneid_filter2, geneid_filter3,TTAA_filter_slider, mis_filter, ois_filter, bm_filter, selected_nodes,clear_clicks,gene_ref_id_filter,class_code_filter):
    """
    Callback to reset the download button n_clicks.

    Parameters:
        - geneid_filter1: Gene ID filter for the first dataset.
        - list: List of gene IDs for filtering.
        - upload_clicks: Number of clicks on the upload button.
        - description_filter: Product description filter.
        - geneid_filter2: Gene ID filter for the second dataset.
        - geneid_filter3: Gene ID filter for the third dataset.
        - TTAA_filter_slider: Range filter for the number of TTAA.
        - mis_filter: Range filter for MIS values.
        - ois_filter: Range filter for OIS values.
        - bm_filter: Range filter for HMS values.
        - selected_nodes: Currently selected network nodes.
        - clear_clicks: Number of clicks on the clear button.

    Returns:
        int or None: Reset n_clicks for the download button.
    """
    return None

@app.callback(
    Output('download-data', 'data'),
    Input('download-button', 'n_clicks'),
    Input('network-nodes-table-filter-GeneIDPkH', 'value'),
    Input('gene-list-store','data'),
   Input('upload-modal-button', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-GeneIDPf3D7', 'value'),
    Input('network-nodes-table-filter-GeneIDPbANKA', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    # Input('network-nodes-table-filter-No_of_TTAA','value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes', 'data'),
    Input('clear-button', 'n_clicks'), 
    Input('network-nodes-table-filter-ref_gene_id', 'value'),
    Input('network-nodes-table-filter-class_code', 'value'),
    prevent_initial_call=True,
)
def update_download_button(n_clicks, geneid_filter1,list,upload_clicks,description_filter, geneid_filter2, geneid_filter3,TTAA_filter_slider, mis_filter, ois_filter, bm_filter, selected_nodes,clear_clicks,gene_ref_id_filter,class_code_filter):
   """
    Callback to update the download button data.

    Parameters:
        - n_clicks: Number of clicks on the download button.
        - geneid_filter1: Gene ID filter for the first dataset.
        - list: List of gene IDs for filtering.
        - upload_clicks: Number of clicks on the upload button.
        - description_filter: Product description filter.
        - geneid_filter2: Gene ID filter for the second dataset.
        - geneid_filter3: Gene ID filter for the third dataset.
        - TTAA_filter_slider: Range filter for the number of TTAA.
        - mis_filter: Range filter for MIS values.
        - ois_filter: Range filter for OIS values.
        - bm_filter: Range filter for HMS values.
        - selected_nodes: Currently selected network nodes.
        - clear_clicks: Number of clicks on the clear button.

    Returns:
        dict or None: Download button data.
    """
   if n_clicks is None:
      PreventUpdate
   if n_clicks is not None:
    df = data.copy()  # Create a copy to avoid modifying the original data
    if clear_clicks:
        df = data.copy()
        csv_string = df.to_csv(index=False, encoding='utf-8')
        return dict(content=csv_string, filename=f"datatable.csv")
    if geneid_filter1 or upload_clicks and not clear_clicks:
        if geneid_filter1 :
           df = df.loc[df['GeneIDPkH'].str.lower().str.contains(geneid_filter1.lower())]
           csv_string = df.to_csv(index=False, encoding='utf-8')
           return dict(content=csv_string, filename=f"{(geneid_filter1)}_table.csv")
        if upload_clicks:
         gene_ids_list = list.split(',')
         df = df.loc[df['GeneIDPkH'].str.lower().isin([gene_id.lower() for gene_id in gene_ids_list])]
         csv_string = df.to_csv(index=False, encoding='utf-8')
         return dict(content=csv_string, filename=f"{','.join(gene_ids_list)}_table.csv")
    if description_filter:
     df = df.loc[df['Product_Description'].str.lower().str.contains(description_filter.lower())]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(description_filter)}_table.csv")
    if TTAA_filter_slider :
     if TTAA_filter_slider :
      df = df.loc[(df['No_of_TTAA'] >= TTAA_filter_slider[0]) & (df['No_of_TTAA'] <= TTAA_filter_slider[1])]
      csv_string = df.to_csv(index=False, encoding='utf-8')
      return dict(content=csv_string, filename=f"No_of_TTAA_range_{TTAA_filter_slider[0]}_{TTAA_filter_slider[1]}_table.csv")
    #  elif TTAA_filter_box:
    #     TTAA_filter = float(TTAA_filter_box) if TTAA_filter_box else 0
        # df = df.loc[df['No_of_TTAA'].astype(float) == TTAA_filter]
    if mis_filter:
      df = df.loc[(df['MIS'] >= mis_filter[0]) & (df['MIS'] <= mis_filter[1])]
      csv_string = df.to_csv(index=False, encoding='utf-8')
      return dict(content=csv_string, filename=f"MIS_range_{mis_filter[0]}_{mis_filter[1]}_table.csv")
    if ois_filter:
     df = df.loc[(df['OIS'] >= ois_filter[0]) & (df['OIS'] <= ois_filter[1])]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"OIS_range_{ois_filter[0]}_{ois_filter[1]}_table.csv")
    if bm_filter:
     df = df.loc[(df['HMS'] >= bm_filter[0]) & (df['HMS'] <= bm_filter[1])]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"HMS_range_{bm_filter[0]}_{bm_filter[1]}_table.csv")
    if geneid_filter2:
      df = df.loc[df['GeneIDPf3D7'].str.lower().str.contains(geneid_filter2.lower(),na=False)]
      csv_string = df.to_csv(index=False, encoding='utf-8')
      return dict(content=csv_string, filename=f"{(geneid_filter2)}_table.csv")
    if geneid_filter3:
     df = df.loc[df['GeneIDPbANKA'].str.lower().str.contains(geneid_filter3.lower(),na=False)]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(geneid_filter3)}_table.csv")
    if gene_ref_id_filter:
     df = df.loc[df['ref_gene_id'].str.lower().str.contains(gene_ref_id_filter.lower(),na=False)]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(gene_ref_id_filter)}_table.csv")
    if class_code_filter:
     df = df.loc[df['class_code'].str.lower().str.contains(class_code_filter.lower(),na=False)]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(class_code_filter)}_table.csv")
    else:
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"datatable.csv")



def create_plot(df, selected_genes, y_column, title):
    """
    Create a plot for selected and unselected genes.

    Parameters:
        - df: DataFrame containing gene data.
        - selected_genes: Name of the selected gene.
        - y_column: Column to be plotted on the y-axis.
        - title: Title of the plot.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object.
    """
    fig = go.Figure()
 # Create a mask to identify the selected genes
    selected_genes_mask = df['GeneIDPkH'] == selected_genes

# Separate the data into selected and unselected genes
    selected_genes_data = df[selected_genes_mask]
    unselected_genes_data = df[~selected_genes_mask]
    grey_plot = go.Scatter(
            x=unselected_genes_data['GeneIndex'],
            y=unselected_genes_data[y_column],
            mode='markers',
            marker=dict(color=unselected_genes_data['GeneIndex'], colorscale=['red', 'white', 'blue'], size=10),
            name="All Genes",
        )
    fig.add_trace(grey_plot)
    fig.update_traces(showlegend=False)

    if selected_genes:
        red_plot = go.Scatter(
            x=selected_genes_data['GeneIndex'],
            y=selected_genes_data[y_column],
            mode='markers',
            marker=dict(color=highlight_color, size=15),
            name=selected_genes
        )
        fig.add_trace(red_plot)

    layout = go.Layout(
           title= f"{y_column} Score",
            showlegend=True,
            xaxis_title='Rank-Ordered Genes',
            plot_bgcolor='white',
        )

    fig.update_layout(layout)
    fig.update_xaxes(showline=True, linecolor='black')
    fig.update_yaxes(showline=True, linecolor='black')
    return fig

def orig_graph(df, y_column, title):
     """
    Create a scatter plot for original gene data.

    Parameters:
        - df: DataFrame containing gene data.
        - y_column: Column to be plotted on the y-axis.
        - title: Title of the plot.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object.
    """
     df['color'] = df['GeneIndex']
     fig1 = px.scatter(df, x='GeneIndex', y=y_column, color=y_column, color_continuous_scale=['red', 'white', 'blue'])
     fig1.update_layout(title=title)
     fig1.update_layout(xaxis_title="Rank-Ordered Genes")
     fig1.update_layout( plot_bgcolor='white')
     fig1.update_xaxes(showline=True, linecolor='black')
     fig1.update_yaxes(showline=True, linecolor='black')
     return fig1
     
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('selected-network-nodes', 'data'),
    Input('network-nodes-table', 'children'),
    
)
def update_graph(selected_cells,table):
    """
    Callback to update the OIS graph based on selected cells in the network table.

    Parameters:
        - selected_cells: List of selected network nodes.
        - table: Children of the network nodes table.

    Returns:
        plotly.graph_objs._figure.Figure: Updated Plotly figure object.
    """
    if not selected_cells:
     fig1 = orig_graph(df_OIS, 'OIS', 'OIS ')
    else:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     fig1 = create_plot(df_OIS, gene_name, 'OIS', 'OIS ')
    return fig1

@app.callback(
    Output('indicator-graphic2', 'figure'),
    Input('selected-network-nodes', 'data'),
    Input('network-nodes-table', 'children'),
    
)

def update_graph2(selected_cells,table):
    """
    Callback to update the MIS graph based on selected cells in the network table.

    Parameters:
        - selected_cells: List of selected network nodes.
        - table: Children of the network nodes table.

    Returns:
        plotly.graph_objs._figure.Figure: Updated Plotly figure object.
    """
    if not selected_cells:
     fig2 = orig_graph(df_MIS, 'MIS', 'MIS ')
    else:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     fig2 = create_plot(df_MIS, gene_name, 'MIS', 'MIS ')
    return  fig2


@app.callback(
    Output('indicator-graphic3', 'figure'),
    Input('selected-network-nodes', 'data'),
    Input('network-nodes-table', 'children'),
    
)

def update_graph2(selected_cells,table):
    """
    Callback to update the HMS graph based on selected cells in the network table.

    Parameters:
        - selected_cells: List of selected network nodes.
        - table: Children of the network nodes table.

    Returns:
        plotly.graph_objs._figure.Figure: Updated Plotly figure object.
    """
    if not selected_cells:
     fig3 = orig_graph(df_HMS, 'HMS', 'HMS')
    else:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     fig3 = create_plot(df_HMS, gene_name, 'HMS', 'HMS')
    return  fig3



@app.callback(
    Output('upload-modal', 'is_open'),
    [Input('open-modal-button', 'n_clicks'),Input('upload-modal-button', 'n_clicks'),],
    [State('upload-modal', 'is_open')]
)
def toggle_modal(open_clicks,upload_clicks,is_open):
    """
    Callback to toggle the upload modal.

    Parameters:
        - open_clicks: Number of clicks on the open modal button.
        - upload_clicks: Number of clicks on the upload modal button.
        - is_open: Current state of the upload modal.

    Returns:
        bool: Updated state of the upload modal.
    """
    if open_clicks or upload_clicks :
        return not is_open
    return is_open

@app.callback(
    # Output('network-nodes-table-filter-GeneIDPkH', 'value'),
    Output('gene-list-store','data'),
    Input('upload-gene-list', 'contents'),
    State('upload-gene-list', 'filename'),
    Input('copy-paste-gene-list', 'value'),
    Input('upload-modal-button', 'n_clicks'), 
    Input('clear-button', 'n_clicks'), 
    prevent_initial_call=True,
)
def update_manual_entry_from_upload(contents, filename, copy_paste_value, upload_clicks,clear):
    """
    Callback to update the gene list from file upload or copy-paste.

    Parameters:
        - contents: Contents of the uploaded file.
        - filename: Name of the uploaded file.
        - copy_paste_value: Value from the copy-paste input field.
        - upload_clicks: Number of clicks on the upload button.
        - clear: Number of clicks on the clear button.

    Returns:
        str: Updated gene list for filtering.
    """
    if upload_clicks is None:
        raise PreventUpdate
    
    if contents is not None and upload_clicks and not clear:
        _, file_extension = os.path.splitext(filename)

        if file_extension.lower() not in ['.csv', '.txt']:
              raise Exception('Unsupported file format')

        content_type, content_string = contents.split(',')  
        decoded = base64.b64decode(content_string)

        try:
            if file_extension.lower() == '.csv':
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif file_extension.lower() == '.txt':
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None, delimiter=',')

                if df.shape[1] == 1:
                    # If there's only one column, use its values as the filter value
                    filter_value = ','.join(df.iloc[:, 0].astype(str).tolist())
                else:
                    # If there are multiple columns, use the first row as column names
                    df.columns = [f'Column_{i}' for i in range(df.shape[1])]
                    filter_value = ','.join(df.iloc[0].astype(str).tolist())
            else:
                raise Exception('Unsupported file format')

            return filter_value

        except Exception as e:
            print(f"Error in update_manual_entry_from_upload: {e}")
            return ''
    elif copy_paste_value and upload_clicks and not clear:
        return copy_paste_value.strip()
    else:
        raise PreventUpdate
    
@app.callback(
    Output('clear-button', 'n_clicks'),
    Input('upload-modal-button', 'n_clicks'), 
    prevent_initial_call=True,  
)
def reset_n_clicks(n):
    """
    Callback to reset the 'Clear' button clicks.

    Parameters:
        - n: Number of clicks on the upload modal button.

    Returns:
        None: Resets the 'Clear' button clicks.
    """
    return None

@app.callback(
   Output('copy-paste-gene-list', 'value'),
   Input('clear-button', 'n_clicks'),
)
def clear_list(n):
   """
    Callback to clear the copy-paste gene list input.

    Parameters:
        - n: Number of clicks on the 'Clear' button.

    Returns:
        str: Empty string to clear the input field.
    """
   if n :
      return ''
      