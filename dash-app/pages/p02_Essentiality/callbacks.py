from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from dash import callback_context 
from pages.components.data_loader import load_data,genome_data,genome
from app import app 
import pandas as pd
import numpy as np
import json
from dash.exceptions import PreventUpdate

highlight_color = 'green'
grey_color = 'lightgrey'
path_mis = 'assets/MIS_sorted.xlsx'
path_ois = 'assets/OIS_sorted.xlsx'
path_hms = 'assets/HMS_sorted.xlsx'
path= 'assets/MIS_OIS_HMS_Pk_Pf_Pb_table_V3_OISMMISlike_rounded.xlsx'

path_bed = r'assets/Pk_5502transcript.bed'
gene_to_genome = genome_data(path_bed)
genome_list = genome(gene_to_genome)
 
df_MIS = load_data(path_mis)
df_OIS = load_data(path_ois)
df_HMS = load_data(path_hms)
data = load_data(path)

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
                    'name': 'GTF track',
                    'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(0,0,255)'
                },
                {
                    'name': 'TTAA Genome Pos',
                    'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
                    'displayMode': 'COLLAPSED',
                    'height': 100,
                    'color': 'rgb(255,0,0)'
                },
            ]


table_columns = [
    {"id": "GeneIDPkH", "name": "GeneIDPkH", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "Product_Description", "name": "Product_Description", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '30%', 'minWidth': '140px'}},
    {"id": "No_of_TTAA", "name": "No_of_TTAA", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "HMS", "name": "HMS", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "GeneIDPf3D7", "name": "GeneIDPf3D7", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '20%', 'minWidth': '140px'}},
    {"id": "GeneIDPbANKA", "name": "GeneIDPbANKA", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '20%', 'minWidth': '140px'}},
]
ctx = callback_context
@app.callback(
    Output('selected-network-nodes', 'data'),
    Input({'type': 'net-node-table-tr', 'index': ALL}, 'n_clicks'),
    Input('network-nodes-table', 'children'),
    Input('selected-network-nodes', 'data')
)
def update_selected_rows(row_n_clicks, table,data):
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


@app.callback(
    Output('network-nodes-table', 'children'),
    Output('network-nodes-table-pagination', 'max_value'),
    Input('network-nodes-table-pagination', 'active_page'),
    Input('network-nodes-table-page-size-radio', 'value'),
    Input('network-nodes-table-filter-GeneIDPkH', 'value'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-GeneIDPf3D7', 'value'),
    Input('network-nodes-table-filter-GeneIDPbANKA', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes', 'data'),
)
def update_info_tables(page, page_size, geneid_filter1,description_filter, geneid_filter2, geneid_filter3,TTAA_filter, mis_filter, ois_filter, bm_filter, selected_nodes):
    page = int(page) - 1

    
    df = data.copy()  # Create a copy to avoid modifying the original data

   
    if geneid_filter1:
        df = df.loc[df['GeneIDPkH'].str.lower().str.contains(geneid_filter1.lower())]
    if description_filter:
        df = df.loc[df['Product_Description'].str.lower().str.contains(description_filter.lower())]
    if TTAA_filter:
        df = df.loc[(df['No_of_TTAA'] >= TTAA_filter[0]) & (df['No_of_TTAA'] <= TTAA_filter[1])]
    if mis_filter:
        df = df.loc[(df['MIS'] >= mis_filter[0]) & (df['MIS'] <= mis_filter[1])]
    if ois_filter:
        df = df.loc[(df['OIS'] >= ois_filter[0]) & (df['OIS'] <= ois_filter[1])]
    if bm_filter:
        df = df.loc[(df['HMS'] >= bm_filter[0]) & (df['HMS'] <= bm_filter[1])]
    if geneid_filter2:
        df = df.loc[df['GeneIDPf3D7'].str.lower().str.contains(geneid_filter2.lower(), na=False)]
    if geneid_filter3:
        df = df.loc[df['GeneIDPbANKA'].str.lower().str.contains(geneid_filter3.lower(), na=False)]


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
    State({'type': 'net-node-table-tr', 'index': MATCH}, 'id'),
    Input('selected-network-nodes', 'data'), )
def update_selected_rows_style(id, data):
    if id['index'] in data:
        style = {"fontWeight": 'bold'}
        className = 'table-active'
    else:
        style = {"fontWeight": 'normal'}
        className = ''
    return style


@app.callback(
    Output('igv-container', 'children'),
    Input('network-nodes-table', 'children'),
    Input('selected-network-nodes', 'data'),
)
def update_igv_locus(table,selected_cells):
    if selected_cells:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     genome_name = gene_to_genome.get(gene_name)
     return html.Div([
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
                ])

    # Handle the case where no rows are selected or the selected index is out of range
    return html.Div([
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
    ])

@app.callback(
    Output('download-button', 'n_clicks'),
    Input('xaxis-value', 'value'),
    Input('mis-slider', 'value'),
    prevent_initial_call=True,  
)
def reset_n_clicks(selected_genes, value):
    return None


# @app.callback(
#     Output('data-download', 'data'),
#     Input('download-button', 'n_clicks'),
#     Input('xaxis-value', 'value'),
#     Input('mis-slider', 'value'),
#     prevent_initial_call=True,
# )
# def update_download_button(n_clicks, selected_genes,value):
#     if n_clicks is None:
#         raise PreventUpdate
#     if selected_genes:
#         filtered_data = data[data['geneID'].isin(selected_genes)]
#         csv_string = filtered_data.to_csv(index=False, encoding='utf-8')
#         return dict(content=csv_string, filename=f"{','.join(selected_genes)}_table.csv")
#     if value:
#      min_mis, max_mis = value
#      filtered_df = data[(data['MIS3'] >= min_mis) & (data['MIS3'] <= max_mis)]
#      csv_string = filtered_df.to_csv(index=False, encoding='utf-8')
#      return dict(content=csv_string, filename=f"MIS_range_{min_mis}_{max_mis}_table.csv")
#     csv_string = data.to_csv(index=False, encoding='utf-8')
#     return dict(content=csv_string, filename=f"datatable.csv")



def create_plot(df, selected_genes, y_column, title):
    fig = go.Figure()
 # Create a mask to identify the selected genes
    selected_genes_mask = df['geneID'] == selected_genes

# Separate the data into selected and unselected genes
    selected_genes_data = df[selected_genes_mask]
    unselected_genes_data = df[~selected_genes_mask]
    grey_plot = go.Scatter(
            x=unselected_genes_data['GeneIndex'],
            y=unselected_genes_data[y_column],
            mode='markers',
            marker=dict(color=grey_color, size=10),
            name='All Genes'
        )
    fig.add_trace(grey_plot)

    if selected_genes:
        red_plot = go.Scatter(
            x=selected_genes_data['GeneIndex'],
            y=selected_genes_data[y_column],
            mode='markers',
            marker=dict(color=highlight_color, size=10),
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
     df['color'] = df['GeneIndex']
     fig1 = px.scatter(df, x='GeneIndex', y=y_column, color=y_column, color_continuous_scale=['blue', 'white', 'red'])
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
    if not selected_cells:
     fig1 = orig_graph(df_OIS, 'OIS', 'OIS Score for Genes')
    else:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     fig1 = create_plot(df_OIS, gene_name, 'OIS', 'OIS Score for Genes')
    return fig1

@app.callback(
    Output('indicator-graphic2', 'figure'),
    Input('selected-network-nodes', 'data'),
    Input('network-nodes-table', 'children'),
    
)

def update_graph2(selected_cells,table):
    if not selected_cells:
     fig2 = orig_graph(df_MIS, 'MIS3', 'MIS Score for Genes')
    else:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     fig2 = create_plot(df_MIS, gene_name, 'MIS3', 'MIS Score for Genes')
    return  fig2


@app.callback(
    Output('indicator-graphic3', 'figure'),
    Input('selected-network-nodes', 'data'),
    Input('network-nodes-table', 'children'),
    
)

def update_graph2(selected_cells,table):
    if not selected_cells:
     fig3 = orig_graph(df_HMS, 'HMS', 'HM Score for Genes')
    else:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
     fig3 = create_plot(df_HMS, gene_name, 'HMS', 'HM Score for Genes')
    return  fig3

