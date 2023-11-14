from dash import Dash, html, dcc, callback, Input, Output, State
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from pages.components.data_loader import load_data,genome_data,genome
from app import app 
import pandas as pd
from pages.components.igv import return_igv
from dash.exceptions import PreventUpdate

highlight_color = 'green'
grey_color = 'lightgrey'
path_mis = 'assets/MIS_sorted.xlsx'
path_ois = 'assets/OIS_sorted.xlsx'
path_bm = 'assets/BM_sorted.xlsx'
path= 'assets/MIS_OIS_BM.xlsx'

path_bed = r'assets\Pk_5502transcript.bed'
gene_to_genome = genome_data(path_bed)
genome_list = genome(gene_to_genome)
 
df_MIS = load_data(path_mis)
df_OIS = load_data(path_ois)
df_BM = load_data(path_bm)
data = load_data(path)

@app.callback(
    Output('igv-container','children'),  
     Input('table', 'selected_rows'),
     State('table','data')
)
def update_igv_locus(selected_rows,table_data):
    if selected_rows:
     selected_row = table_data[selected_rows[0]]
     selected_genes = selected_row['geneID']
    #  selected_genes_str = f"'{selected_genes}'"
     genome_name = gene_to_genome.get(selected_genes)
     print(selected_genes)
     return html.Div([
        dashbio.Igv(
        # id='igv-container',
        locus = genome_name,
        reference={
            'id': "Id",
            'name': "PKHN",
            'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
            'indexURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
            'order': 1000000,
            'tracks': [
                {
                    'name': 'TTAA Track',
                    'url': app.get_asset_url('75Pk_20231022_TTAA.sorted.bam'),
                    'indexURL': app.get_asset_url('75Pk_20231022_TTAA.sorted.bai'),
                    'displayMode': 'EXPANDED',
                    'nameField': 'gene',
                    'height': 150,
                    'color': 'rgb(169, 169, 169)'
                },
                {
                    'name': 'TTAA Genome Pos',
                    'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
                    'displayMode': 'COLLAPSED',
                    'height': 100,
                    'color': 'rgb(255,0,0)'
                },
                {
                    'name': 'GTF track',
                    'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(0,0,255)'
                }
            ]
         }
         )])

    return html.Div([
       dashbio.Igv(
        # id='igv-container',
        genome= genome_list,
        reference={
            'id': "Id",
            'name': "PKHN",
            'fastaURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta'),
            'indexURL': app.get_asset_url('PlasmoDB-58_PknowlesiH_Genome.fasta.fai'),
            'order': 1000000,
            'tracks': [
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
                    'name': 'TTAA Genome Pos',
                    'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
                    'displayMode': 'COLLAPSED',
                    'height': 100,
                    'color': 'rgb(255,0,0)'
                },
                {
                    'name': 'GTF track',
                    'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(0,0,255)'
                }
            ]
        }
    )
    ])


     
# @app.callback(
#     Output('table', 'data'),
#     Input('xaxis-value', 'value'),
# )
# def update_table(selected_genes):
#     if selected_genes:
#         filtered_data = data[data['geneID'].isin(selected_genes)]
#         return filtered_data.to_dict('records') 
#     return data.to_dict('records')
# @app.callback(
#     Output('data-download', 'data'),
#     Input('download-button', 'n_clicks'),
#     Input('xaxis-value', 'value'),
# )
# def update_download_button(n_clicks, selected_genes):
#     if n_clicks is None:
#         raise PreventUpdate
    
#     if selected_genes:
#         filtered_data = data[data['geneID'].isin(selected_genes)]
#         csv_string = filtered_data.to_csv(index=False, encoding='utf-8')
#         return dict(content=csv_string, filename=f"{','.join(selected_genes)}_table.csv")
#     else:
#         raise PreventUpdate

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
    Input('table', 'selected_rows'),
    State('table','data')
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
    Input('table', 'selected_rows'),
    State('table','data')
)

def update_graph2(selected_rows,table_data):
    if not selected_rows:
     fig2 = orig_graph(df_MIS, 'MIS3', 'MIS Score for Genes')
    else:
     selected_row = table_data[selected_rows[0]]
     selected_gene = selected_row['geneID']
     fig2 = create_plot(df_MIS, selected_gene, 'MIS3', 'MIS Score for Genes')
    return  fig2


@app.callback(
    Output('indicator-graphic3', 'figure'),
    Input('table', 'selected_rows'),
    State('table','data')
)

def update_graph2(selected_rows,table_data):
    if not selected_rows:
     fig3 = orig_graph(df_BM, 'BM', 'BM Score for Genes')
    else:
     selected_row = table_data[selected_rows[0]]
     selected_gene = selected_row['geneID']
     fig3 = create_plot(df_BM, selected_gene, 'BM', 'BM Score for Genes')
    return  fig3

