from dash import dcc


def dropdown_selected_gene(data):
    options = [{'label': gene, 'value': gene} for gene in data['geneID'].unique()]
    return dcc.Dropdown(
        options=options,
        id='xaxis-value',
        multi=True,
        placeholder="Select gene ID to filter",
        style={'width': '300px'}
    )