from dash import Dash, html, dcc, callback, Input, Output, State
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from pages.components.data_loader import load_data
from app import app 
import pandas as pd
from pages.components.igv import return_igv

highlight_color = 'green'
grey_color = 'lightgrey'
path_mis = 'assets/MIS_sorted.xlsx'
path_ois = 'assets/OIS_sorted.xlsx'
path_bm = 'assets/BM_sorted.xlsx'
path= 'assets/MIS_OIS_BM.xlsx'

# path_bed = r'D:\Demo_App\dash-app\assets\Pk_5502transcript.bed'
# gene_to_region = locus_data(path_bed)
 
df_MIS = load_data(path_mis)
df_OIS = load_data(path_ois)
df_BM=load_data(path_bm)
data = load_data(path)

# @app.callback(
#     Output('igv-container', 'locus'),  # Update the 'locus' property of the IGV component
#     Input('xaxis-value', 'value')  # Listen to changes in the dropdown selection
# )
# def update_igv_locus(selected_genes):
#     # Add your logic here to determine the locus based on the selected genes
#     # For example, if you want to show the locus of the first selected gene:
#      if selected_genes:
#       first_selected_gene = selected_genes[0]
#       genomic_region = gene_to_region.get(first_selected_gene,'PKNH_14_v2:209-2791') 
#       return genomic_region
     
@app.callback(
    Output('table', 'data'),
    Input('xaxis-value', 'value'),
)
def update_table(selected_genes):
    if selected_genes:
        filtered_data = data[data['geneID'].isin(selected_genes)]
        return filtered_data.to_dict('records') 
    return []

def create_plot(df, selected_genes, y_column, title):
    fig = go.Figure()
 # Create a mask to identify the selected genes
    selected_genes_mask = df['geneID'].isin(selected_genes)

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

    for value in selected_genes:
            filtered_df = selected_genes_data[selected_genes_data['geneID'] == value]
            red_plot = go.Scatter(
                x=filtered_df['GeneIndex'],
                y=filtered_df[y_column],
                mode='markers',
                marker=dict(color=highlight_color, size=10),
                name=value
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
    Input('xaxis-value', 'value'),
)
def update_graph(selected_gene):
    if not selected_gene:
     fig1 = orig_graph(df_OIS, 'OIS', 'OIS Score for Genes')
    else:
     fig1 = create_plot(df_OIS, selected_gene, 'OIS', 'OIS Score for Genes')
    return fig1

@app.callback(
    Output('indicator-graphic2', 'figure'),
    Input('xaxis-value', 'value'),
)

def update_graph2(selected_gene):
    if not selected_gene:
     fig2 = orig_graph(df_MIS, 'MIS3', 'MIS Score for Genes')
    else:
     fig2 = create_plot(df_MIS, selected_gene, 'MIS3', 'MIS Score for Genes')
    return  fig2

@app.callback(
    Output('indicator-graphic3', 'figure'),
    Input('xaxis-value', 'value'),
)
def update_graph3(selected_gene):
    if not selected_gene:
     fig3 = orig_graph(df_BM,  'BM', 'BM Score for Genes') 
    else:
     fig3 = create_plot(df_BM, selected_gene, 'BM', 'BM Score for Genes')
    return fig3
