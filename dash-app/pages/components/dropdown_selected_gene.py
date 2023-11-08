from dash import dcc


def dropdown_selected_gene(data):
    options = [{'label': gene, 'value': gene} for gene in data['geneID'].unique()]
    return dcc.Dropdown(
        options=options,
        id='xaxis-value',
        multi=True
    )
#  return dcc.Dropdown(
#         id='xaxis-value',
#         options=[{'label': gene_name, 'value': gene_name} for gene_name in gene_to_region.keys()],
#         value=list(gene_to_region.keys())[0]  # Set the initial value
#     ),
