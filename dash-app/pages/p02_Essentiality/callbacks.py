from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from dash import callback_context as ctx
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
path_bm = 'assets/BM_sorted.xlsx'
path= 'assets/MIS_OIS_HMS_Pk_Pf_Pb_table_V2.xlsx'

path_bed = r'assets\Pk_5502transcript.bed'
gene_to_genome = genome_data(path_bed)
genome_list = genome(gene_to_genome)
 
df_MIS = load_data(path_mis)
df_OIS = load_data(path_ois)
df_BM = load_data(path_bm)
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
    {"id": "GeneID.PkH", "name": "GeneID.PkH", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "Product.Description", "name": "Product.Description", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '40%', 'minWidth': '140px'}},
    {"id": "No.of_TTAA", "name": "No.of_TTAA", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "HMS", "name": "BM", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "GeneID.Pf_3D7", "name": "GeneID.Pf_3D7", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {"id": "GeneID.Pb_ANKA", "name": "GeneID.Pb_ANKA", "editable": False,'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
]
@app.callback(
    Output('selected-network-nodes', 'data'),
    Input({'type': 'net-node-table-tr', 'index': ALL}, 'n_clicks'),
    Input('selected-network-nodes', 'data'),
)
def update_selected_rows(row_n_clicks, data):
    index = None  # Initialize index
    if ctx.triggered[0]['prop_id'] == '.':
        raise PreventUpdate
    if ctx.triggered[0]['prop_id'] == 'network-nodes-table.children':
        if data == [0]:
            raise PreventUpdate
        return [0]
    if len(ctx.triggered) == 1:
        id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        id = json.loads(id_str)
        index = id['index']
    if index is not None and index not in data:
        data.append(index)
    elif index is not None:
        data.remove(index)
    return data


@app.callback(
    Output('network-nodes-table', 'children'),
    Output('network-nodes-table-pagination', 'max_value'),
    Output('network-nodes-table-filter-MIS-form-message', 'children'),
    Output('network-nodes-table-filter-OIS-form-message', 'children'),
    Input('network-nodes-table-pagination', 'active_page'),
    Input('network-nodes-table-page-size-radio', 'value'),
    Input('network-nodes-table-filter-GeneIDPkH', 'value'),
    Input('network-nodes-table-filter-MIS', 'value'),
    Input('network-nodes-table-filter-OIS', 'value'),
    Input('network-nodes-table-filter-HMS', 'value'),
    State('network-nodes-table-sort-column-values-state', 'data'),
    State('selected-network-nodes', 'data'),
)
def update_info_tables(page, page_size, geneid_filter, mis_filter, ois_filter, bm_filter, sort_state, selected_nodes):
    page = int(page) - 1

    # Assuming 'data' is your provided data
    df = data

    if geneid_filter:
        df = df.loc[df['GeneID.PkH'].str.lower().str.contains(geneid_filter.lower())]
    if mis_filter:
        df = df.loc[(df['MIS'] >= mis_filter[0]) & (df['MIS'] <= mis_filter[1])]
    if ois_filter:
        df = df.loc[(df['OIS'] >= ois_filter[0]) & (df['OIS'] <= ois_filter[1])]
    if bm_filter:
        df = df.loc[df['HMS'].str.lower().str.contains(bm_filter.lower())]

    by = [c['id'] for i, c in enumerate(table_columns) if sort_state[i] > 0]
    ascending = [not bool(s - 1) for s in sort_state if s > 0]
    df = df.sort_values(by, ascending=ascending)

    data_slice = [{'index': i, 'GeneID.PkH': '', 'Product.Description': ''} for i in range(page * page_size, (page + 1) * page_size)]
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
    degree_form_message = f'Showing values between {mis_filter}' if mis_filter else ''
    zscore_form_message = f'Showing values between {ois_filter}' if ois_filter else ''

    return net_body, int(np.ceil(filtered_data_nrows / page_size)), degree_form_message, zscore_form_message



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
    Input('network-nodes-table', 'selected_rows'),
    State('selected-network-nodes', 'data'),
)
def update_igv_locus(selected_cells, table_data):
    print("Callback Activated!")
    print("Selected Cells:", selected_cells)
    print(table_data)
    print("Callback Context:", ctx.triggered_id, ctx.inputs, ctx.states)
    if selected_cells:
        selected_cell = selected_cells[0]

        # Check if the selected cell is within the valid range
        if selected_cell is not None and selected_cell['row'] < len(table_data):
            selected_row = table_data[selected_cell['row']]
            selected_genes = selected_row.get('geneID')
            genome_name = gene_to_genome.get(selected_genes)
            print(f"Selected Genes: {selected_genes}")
            print(f"Genome Name: {genome_name}")
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

     
# @app.callback(
#     Output('table', 'data'),
#     [Input('xaxis-value', 'value'),Input('mis-slider', 'value')],
# )
# def update_table(selected_genes,value):
#     if selected_genes:
#         filtered_data = data[data['geneID'].isin(selected_genes)]
#         return filtered_data.to_dict('records') 
#     if value:
#       min_mis, max_mis = value
#       filtered_df = data[(data['MIS3'] >= min_mis) & (data['MIS3'] <= max_mis)]
#       return filtered_df.to_dict('records')
#     else :
#      return  data.to_dict('records') 
    
# @app.callback(
#     Output('download-button', 'n_clicks'),
#     Input('xaxis-value', 'value'),
#     Input('mis-slider', 'value'),
#     prevent_initial_call=True,  
# )
# def reset_n_clicks(selected_genes, value):
#     return None


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
    Input('network-nodes-table', 'selected_rows'),
     State('selected-network-nodes', 'data'),
)
def update_graph(selected_rows,table_data):
    if not selected_rows:
     fig1 = orig_graph(df_OIS, 'OIS', 'OIS Score for Genes')
    else:
     selected_row = table_data[selected_rows[0]]
     selected_gene = selected_row['geneID']
     fig1 = create_plot(df_OIS, selected_gene, 'OIS', 'OIS Score for Genes')
    return fig1

@app.callback(
    Output('indicator-graphic2', 'figure'),
    Input('network-nodes-table', 'selected_rows'),
    State('selected-network-nodes', 'data'),
)

def update_graph2(selected_rows,table_data):
    if not selected_rows:
     fig2 = orig_graph(df_MIS, 'MIS3', 'MIS Score for Genes')
    else:
     selected_row = table_data[selected_rows[0]]
     selected_gene = selected_row['geneID']
     fig2 = create_plot(df_MIS, selected_gene, 'MIS', 'MIS Score for Genes')
    return  fig2


@app.callback(
    Output('indicator-graphic3', 'figure'),
    Input('network-nodes-table', 'selected_cells'),
     State('selected-network-nodes', 'data'),
)

def update_graph2(selected_rows,table_data):
    if not selected_rows:
     fig3 = orig_graph(df_BM, 'BM', 'HM Score for Genes')
    else:
     selected_row = table_data[selected_rows[0]]
     selected_gene = selected_row['geneID']
     fig3 = create_plot(df_BM, selected_gene, 'BM', 'BM Score for Genes')
    return  fig3

