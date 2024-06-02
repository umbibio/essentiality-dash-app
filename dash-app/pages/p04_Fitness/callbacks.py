from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from dash import callback_context 
import pages.components.fitness_data_plots as fdata
from pages.components.data_loader import load_data
from app import app 
import pandas as pd
import os
import base64
import io
import numpy as np
import json
from dash.exceptions import PreventUpdate
import statsmodels.api as sm

path= 'assets/fitness_page_table_sheet.xlsx'
data = load_data(path).round(3)
# data["MFS.slope"] = data["MFS.slope"].round(3)
# Define table columns
table_columns = [
    {"id": "geneID", "name": "GeneID", "editable": False,'header_style': {'width': '25%', }, 'style': {'width': '15%', }},
    {"id": "MFS.slope", "name": "FIS", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '10%', }},
    {"id": "lm.p.value", "name": "lm.p.value", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '15%', }},
    {"id": "lm.adjusted.p.value", "name": "lm.adjusted.p.value", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '15%', }},
     {"id": "Product.Description", "name": "Product_Description", "editable": False,'header_style': {'width': '25%', }, 'style': {'width': '25%', }},
    {"id": "e.pvalue", "name": "e.pvalue", "editable": False,'header_style': {'width': '12%', }, 'style': {'width': '15%', }},
]


# Define the Dash app callback context
ctx = callback_context
# Define the callback for updating selected network nodes
@app.callback(
    Output('selected-network-nodes-ft', 'data'),
    Input({'type': 'net-node-table-ft-tr', 'index': ALL}, 'n_clicks'),
    Input('network-nodes-table-ft', 'children'),
    Input('selected-network-nodes-ft', 'data'),
)
def update_selected_rows(row_n_clicks, table,data):
    """
    Callback to update the list of selected network nodes.

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
    Output('network-nodes-table-ft', 'children'),
    Output('network-nodes-table-pagination-ft', 'max_value'),
    Input('network-nodes-table-pagination-ft', 'active_page'),
    Input('network-nodes-table-page-size-radio-ft', 'value'),
    Input('gene-list-store-ft','data'),
    Input('upload-modal-button-ft', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-GeneID', 'value'),
    Input('MFS_slope-slider', 'value'),
    Input('lm_p_value-slider', 'value'),
    Input('lm_adjusted_p_value-slider', 'value'),
    Input('e_pvalue-slider', 'value'),
    State('selected-network-nodes-ft', 'data'),
    Input('clear-button-ft', 'n_clicks'), 
)
def update_info_tables(page, page_size,gene_list,upload_clicks,description_filter,geneid_filter1,MFS_Slope_slider, lm_p_filter, lm_p_adj_filter, e_p_filter, selected_nodes,clear_clicks):
    """
    Callback to update the network nodes table and pagination.


    Returns:
        Tuple: Updated network nodes table and maximum pagination value.
    """
    page = int(page) - 1

    
    df = data.copy()  # Create a copy to avoid modifying the original data
    if clear_clicks:
        df = data.copy()
    if geneid_filter1 or upload_clicks and not clear_clicks:
        if geneid_filter1 :
           df = df.loc[df['geneID'].str.lower().str.contains(geneid_filter1.lower(),na=False)]
        if upload_clicks:
         gene_ids_list = gene_list.split(',')
         print(type(gene_list))
         df = df.loc[df['geneID'].str.lower().isin([gene_id.lower() for gene_id in gene_ids_list])]
    if description_filter:
     df = df.loc[df['Product_Description'].str.lower().str.contains(description_filter.lower(),na=False)]
    if MFS_Slope_slider :
      df = df.loc[(df['MFS.slope'] >= MFS_Slope_slider[0]) & (df['MFS.slope'] <= MFS_Slope_slider[1])]
    if lm_p_filter:
      df = df.loc[(df[''] >= lm_p_filter[0]) & (df['lm.p.value'] <= lm_p_filter[1])]
    if lm_p_adj_filter:
     df = df.loc[(df['lm.adjusted.p.value'] >= lm_p_adj_filter[0]) & (df['lm.adjusted.p.value'] <= lm_p_adj_filter[1])]
    if e_p_filter:
     df = df.loc[(df['e.pvalue'] >= e_p_filter[0]) & (df['e.pvalue'] <= e_p_filter[1])]


    data_slice = [{'index': i, 'GeneID': '', 'Product_Description': ''} for i in range(page * page_size, (page + 1) * page_size)]
    for i, item in enumerate(df.iloc[page * page_size:(page + 1) * page_size].to_dict('records')):
        item_with_index = {'index': i, **item}
        data_slice[i].update(item_with_index)

    net_body = [
        html.Tbody([
            html.Tr([
                html.Td(item_with_index.get(c['id'], '-'), style=c['style'])
                for c in table_columns],
                id={'type': 'net-node-table-ft-tr', 'index': item_with_index['index']},
                style={"fontWeight": 'bold'} if item_with_index['index'] in selected_nodes else {
                    "fontWeight": 'normal'},
                className='table-active-ft' if item_with_index['index'] in selected_nodes else '', )
            for item_with_index in data_slice
        ])
    ]

    filtered_data_nrows = len(df)

    return net_body, int(np.ceil(filtered_data_nrows / page_size))


@app.callback(
    Output('download-button-ft', 'n_clicks'),
   Input('gene-list-store-ft','data'),
    Input('upload-modal-button-ft', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-GeneID', 'value'),
    Input('MFS_slope-slider', 'value'),
    Input('lm_p_value-slider', 'value'),
    Input('lm_adjusted_p_value-slider', 'value'),
    Input('e_pvalue-slider', 'value'),
    State('selected-network-nodes-ft', 'data'),
    Input('clear-button-ft', 'n_clicks'), 

    prevent_initial_call=True,
) 
def reset_n_clicks(list,upload_clicks,description_filter, geneid_filter1,MFS_Slope_slider, lm_p_filter, lm_p_adj_filter, e_p_filter, selected_nodes,clear_clicks ):
    """
    Callback to reset the download button n_clicks.

   
    Returns:
        int or None: Reset n_clicks for the download button.
    """
    return None

@app.callback(
    Output({'type': 'net-node-table-ft-tr', 'index': MATCH}, 'style'),
    Output({'type': 'net-node-table-ft-tr', 'index': MATCH}, 'className'),
    State({'type': 'net-node-table-ft-tr', 'index': MATCH}, 'id'),
    Input('selected-network-nodes-ft', 'data'), )
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
        className = 'table-active-ft'
    else:
        style = {"fontWeight": 'normal'}
        className = ''
    return style,className

@app.callback(
    Output('upload-modal-ft', 'is_open'),
    [Input('open-modal-button-ft', 'n_clicks'),Input('upload-modal-button-ft', 'n_clicks'),],
    [State('upload-modal-ft', 'is_open')]
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
    Output('gene-list-store-ft','data'),
    Input('upload-gene-list-ft', 'contents'),
    State('upload-gene-list-ft', 'filename'),
    Input('copy-paste-gene-list-ft', 'value'),
    Input('upload-modal-button-ft', 'n_clicks'), 
    Input('clear-button-ft', 'n_clicks'), 
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
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8'), observed=False))
            elif file_extension.lower() == '.txt':
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None, delimiter=',', observed=False)

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
    Output('clear-button-ft', 'n_clicks'),
    Input('upload-modal-button-ft', 'n_clicks'), 
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
   Output('copy-paste-gene-list-ft', 'value'),
   Input('clear-button-ft', 'n_clicks'),
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
   
   
@app.callback(
    Output('scatter-plot-ft', 'figure'),
    Input('selected-network-nodes-ft', 'data'),
    Input('network-nodes-table-ft', 'children'), 
)
def update_scatter_plot(selected_cells,table):
    if selected_cells:
         selected_index = selected_cells[0]
         row = table[0]['props']['children'][selected_index]['props']['children']
         gene = row[0]
         gene_name = gene['props']['children']
         # selected_df = fdata.df2[fdata.df2['geneID'].isin(selected_cells)]
         gene_df = fdata.df2[fdata.df2['geneID'] == gene_name]
    #     fig.update_yaxes(range=[-1, 0.5])
         fdata.df2['selected'] = (fdata.df2['geneID'] == gene_name)

# Define colors based on whether the point belongs to the selected gene or not
         colors = ['#13B187' if selected else 'grey' for selected in fdata.df2['selected']]

# Create the scatter plot
         fig = go.Figure(data=go.Scatter(
         x=fdata.df2['HMS'], y=fdata.df2['MFS.slope'],
         mode='markers', marker=dict(color=colors, size=8),
        hoverinfo='text',  # Show text on hover
      text=fdata.df2['geneID'] + '<br>' +  
           'HMS: ' + fdata.df2['HMS'].astype(str) + '<br>' +  
         'MFS Slope: ' + fdata.df2['MFS.slope'].astype(str),showlegend=False
  ))
         fig.add_trace(go.Scatter(
            x=gene_df['HMS'], y=gene_df['MFS.slope'],
            mode='markers', marker=dict(color='#13B187', size=8), name=gene_name,
            hoverinfo='text',  # Show text on hover
            text=gene_df['geneID'] + '<br>' +  
                 'HMS: ' + gene_df['HMS'].astype(str) + '<br>' +  
                 'MFS Slope: ' + gene_df['MFS.slope'].astype(str),showlegend=True
        ))
         # add epvalue and lmadjustedp

# Add vertical lines
         fig.add_vline(x=fdata.kneepoints1, line=dict(dash='dash', color='#C63135', width=1.2))
         fig.add_vline(x=fdata.kneepoints2, line=dict(dash='dash', color='#237AB6', width=1.2))

# Add horizontal lines
         fig.add_hline(y=fdata.c1_Fslope_ep, line=dict(dash='dash', color='pink', width=1.2))
         fig.add_hline(y=fdata.c2_Fslope_ep, line=dict(dash='dash', color='#E3770C', width=1.2))
         fig.add_hline(y=0, line=dict(dash='dash', color='black', width=1))

# Set y-axis limits
         fig.update_yaxes(range=[-1, 0.5])

# Update layout
         fig.update_layout(
      template='plotly_white',
      xaxis_title='HMS',
    #   yaxis_title='Fitness Index Score',
      title='Fitness Index Score vs HMS',
      legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        x=0.6, y=0.4
      ),
       margin=dict(l=0, r=0, t=30, b=0),
       plot_bgcolor='white',
       legend_title_text=None,
       font=dict(color='black', size=18),  # Update axis and label font properties
       yaxis=dict(tickfont=dict(color='black'))
       )
    else:
        fig = fdata.fig

    return fig

@app.callback(
Output('trending-plot-container', 'children'),
[    Input('selected-network-nodes-ft', 'data'),
    Input('network-nodes-table-ft', 'children'),
      Input('gene-list-store-ft','data'), ],
)
def trending_plot(input_gene_list,table,uploaded):
    if not input_gene_list and not uploaded :
      figures=fdata.trendingPlot(fdata.Input_gene_list) 
    elif input_gene_list:
        selected_index = int(input_gene_list[0]) 
        row = table[0]['props']['children'][selected_index]['props']['children']
        gene = row[0]
        gene_name_elements = gene['props']['children']
        if isinstance(gene_name_elements, list):
            gene_name = ''.join(gene_name_elements)
        else:
            gene_name = gene_name_elements
        figures=fdata.trendingPlot([gene_name])
    elif uploaded : 
      print(uploaded)
      if isinstance(input_gene_list, str):
          input_gene_list = [gene.strip() for gene in input_gene_list.split(',') if gene.strip()]
          print(input_gene_list)
          figures= fdata.trendingPlot(input_gene_list)
    
    graph_columns = [dbc.Col(dcc.Graph(id=f'trending-plot-ft-{i}', figure=fig)) for i, fig in enumerate(figures)]

    return graph_columns
   
