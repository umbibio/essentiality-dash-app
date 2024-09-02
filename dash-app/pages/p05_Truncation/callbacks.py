from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from dash import callback_context 
from pages.components.data_loader import load_data
from app import app 
import pandas as pd
import os
import base64
import io
import numpy as np
import json
from dash.exceptions import PreventUpdate
from pages.components import truncation_data as td

path= 'assets/truncation_page_table.xlsx'
data = load_data(path)
columns_to_round = ["cp","MSE","R_i",'HMS', 'MIS', 'OIS']
data[columns_to_round] = data[columns_to_round].round(3)

table_columns = [
    {"id": "geneID", "name": "GeneID", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "Product_Description", "name": "Product.Description", "editable": False,'header_style': {'width': '16%', }, 'style': {'width': '16%', }},
    {"id": "Symbol", "name": "Symbol", "editable": False,'header_style': {'width': '7%', }, 'style': {'width': '7%', }},
    {"id": "cp", "name": "cp", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "MSE", "name": "MSE", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "R_i", "name": "R_i", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
     {"id": "TTAA", "name": "TTAA", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "MIS", "name": "MIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "OIS", "name": "OIS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "HMS", "name": "HMS", "editable": False,'header_style': {'width': '5%', }, 'style': {'width': '5%', }},
    {"id": "Truncation_type", "name": "Truncation_type", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
    {"id": "MSE_cutoff", "name": "MSE_cutoff", "editable": False,'header_style': {'width': '10%', }, 'style': {'width': '10%', }},
]

# Define the Dash app callback context
ctx = callback_context
# Define the callback for updating selected network nodes
@app.callback(
    Output('selected-network-nodes-trunc', 'data'),
    Input({'type': 'net-node-table-trunc-tr', 'index': ALL}, 'n_clicks'),
    Input('network-nodes-table-trunc', 'children'),
    Input('selected-network-nodes-trunc', 'data'),
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
    # if ctx.triggered and ctx.triggered[0]['prop_id'] != '.':
    #     id_str = ctx.triggered[0]['prop_id'].split('.')[0]
    #     if id_str:
    #         try:
    #             id = json.loads(id_str)
    #             index = id.get('index')
    #         except json.JSONDecodeError:
    #             index = None
    #     if index is not None:
    #         data = [index]  # Replace the current selection with the new one
    # return data

# Define the callback for updating network nodes table and pagination
@app.callback(
    Output('network-nodes-table-trunc', 'children'),
    Output('network-nodes-table-pagination-trunc', 'max_value'),
    Input('network-nodes-table-pagination-trunc', 'active_page'),
    Input('network-nodes-table-page-size-radio-trunc', 'value'),
    Input('network-nodes-table-filter-geneID', 'value'),
    Input('gene-list-store-trunc','data'),
    Input('upload-modal-button-trunc', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-symbol', 'value'),
    Input('network-nodes-table-filter-Truncation_type', 'value'),
    Input('network-nodes-table-filter-MSE_cutoff', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    # Input('network-nodes-table-filter-No_of_TTAA','value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes-trunc', 'data'),
    Input('clear-button-trunc', 'n_clicks'), 
   Input('cp-slider', 'value'),
   Input('MSE-slider', 'value'),
   Input('R_i-slider', 'value'),
)
def update_info_tables(page, page_size, geneid_filter1,list,upload_clicks,description_filter,symbol_filter, truncation_type_filter, MSE_cuttoff_filter,TTAA_filter_slider, mis_filter, ois_filter, bm_filter, selected_nodes,clear_clicks,cp_filter,MSE_filter,R_i_filter):
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
           df = df.loc[df['geneID'].str.lower().str.contains(geneid_filter1.lower(),na=False)]
        if upload_clicks:
         gene_ids_list = list.split(',')
         df = df.loc[df['geneID'].str.lower().isin([gene_id.lower() for gene_id in gene_ids_list])]
    if description_filter:
     df = df.loc[df['Product_Description'].str.lower().str.contains(description_filter.lower(),na=False)]
    if symbol_filter:
     df = df.loc[df['Symbol'].str.lower().str.contains(symbol_filter.lower(),na=False)]
    if TTAA_filter_slider :
     if TTAA_filter_slider :
      df = df.loc[(df['TTAA'] >= TTAA_filter_slider[0]) & (df['TTAA'] <= TTAA_filter_slider[1])]
    #  elif TTAA_filter_box:
    #     TTAA_filter = float(TTAA_filter_box) if TTAA_filter_box else 0
        # df = df.loc[df['No_of_TTAA'].astype(float) == TTAA_filter]
    if mis_filter:
      df = df.loc[(df['MIS'] >= mis_filter[0]) & (df['MIS'] <= mis_filter[1])]
    if ois_filter:
     df = df.loc[(df['OIS'] >= ois_filter[0]) & (df['OIS'] <= ois_filter[1])]
    if bm_filter:
     df = df.loc[(df['HMS'] >= bm_filter[0]) & (df['HMS'] <= bm_filter[1])]
    if truncation_type_filter:
      df = df.loc[df['Truncation_type'].str.lower().str.contains(truncation_type_filter.lower(),na=False)]
    if MSE_cuttoff_filter:
     df = df.loc[df['MSE_cutoff'].str.lower().str.contains(MSE_cuttoff_filter.lower(),na=False)]
    if cp_filter:
     df = df.loc[(df['cp'] >= cp_filter[0]) & (df['cp'] <= cp_filter[1])]
    if MSE_filter:
     df = df.loc[(df['MSE'] >= MSE_filter[0]) & (df['MSE'] <= MSE_filter[1])]
    if R_i_filter:
     df = df.loc[(df['R_i'] >= R_i_filter[0]) & (df['R_i'] <= R_i_filter[1])]
    

    data_slice = [{'index': i, 'geneID': '', 'Product_Description': ''} for i in range(page * page_size, (page + 1) * page_size)]
    for i, item in enumerate(df.iloc[page * page_size:(page + 1) * page_size].to_dict('records')):
        item_with_index = {'index': i, **item}
        data_slice[i].update(item_with_index)

    net_body = [
        html.Tbody([
            html.Tr([
                html.Td(item_with_index.get(c['id'], '-'), style=c['style'])
                for c in table_columns],
                id={'type': 'net-node-table-trunc-tr', 'index': item_with_index['index']},
                style={"fontWeight": 'bold'} if item_with_index['index'] in selected_nodes else {
                    "fontWeight": 'normal'},
                className='table-active' if item_with_index['index'] in selected_nodes else '', )
            for item_with_index in data_slice
        ])
    ]

    filtered_data_nrows = len(df)

    return net_body, int(np.ceil(filtered_data_nrows / page_size))




@app.callback(
    Output({'type': 'net-node-table-trunc-tr', 'index': MATCH}, 'style'),
    Output({'type': 'net-node-table-trunc-tr', 'index': MATCH}, 'className'),
    State({'type': 'net-node-table-trunc-tr', 'index': MATCH}, 'id'),
    Input('selected-network-nodes-trunc', 'data'), )
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
    Output('download-button-trunc', 'n_clicks'),
    Input('network-nodes-table-filter-geneID', 'value'),
    Input('gene-list-store-trunc','data'),
   Input('upload-modal-button-trunc', 'n_clicks'),
   Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-symbol', 'value'),
    Input('network-nodes-table-filter-Truncation_type', 'value'),
    Input('network-nodes-table-filter-MSE_cutoff', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    # Input('network-nodes-table-filter-No_of_TTAA','value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes-trunc', 'data'),
    Input('clear-button-trunc', 'n_clicks'), 
    Input('cp-slider', 'value'),
   Input('MSE-slider', 'value'),
   Input('R_i-slider', 'value'),

    prevent_initial_call=True,
) 
def reset_n_clicks(geneid_filter1,list,upload_clicks,description_filter, symbol_filter,truncation_type_filter, MSE_cuttoff_filter,TTAA_filter_slider, mis_filter, ois_filter, bm_filter, selected_nodes,clear_clicks,p_filter,MSE_filter,R_i_filter):
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
    Output('download-data-trunc', 'data'),
    Input('download-button-trunc', 'n_clicks'),
    Input('network-nodes-table-filter-geneID', 'value'),
    Input('gene-list-store-trunc','data'),
   Input('upload-modal-button-trunc', 'n_clicks'),
    Input('network-nodes-table-filter-Product_Description', 'value'),
    Input('network-nodes-table-filter-symbol', 'value'),
    Input('network-nodes-table-filter-Truncation_type', 'value'),
    Input('network-nodes-table-filter-MSE_cutoff', 'value'),
    Input('No_of_TTAA-slider', 'value'),
    # Input('network-nodes-table-filter-No_of_TTAA','value'),
    Input('MIS-slider', 'value'),
    Input('OIS-slider', 'value'),
    Input('HMS-slider', 'value'),
    State('selected-network-nodes-trunc', 'data'),
    Input('clear-button-trunc', 'n_clicks'), 
   Input('cp-slider', 'value'),
   Input('MSE-slider', 'value'),
   Input('R_i-slider', 'value'),
    prevent_initial_call=True,
)
def update_download_button(n_clicks, geneid_filter1,list,upload_clicks,description_filter,symbol_filter, truncation_type_filter, MSE_cuttoff_filter,TTAA_filter_slider, mis_filter, ois_filter, bm_filter, selected_nodes,clear_clicks,cp_filter,MSE_filter,R_i_filter):
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
           df = df.loc[df['geneID'].str.lower().str.contains(geneid_filter1.lower())]
           csv_string = df.to_csv(index=False, encoding='utf-8')
           return dict(content=csv_string, filename=f"{(geneid_filter1)}_table.csv")
        if upload_clicks:
         gene_ids_list = list.split(',')
         df = df.loc[df['geneID'].str.lower().isin([gene_id.lower() for gene_id in gene_ids_list])]
         csv_string = df.to_csv(index=False, encoding='utf-8')
         return dict(content=csv_string, filename=f"{','.join(gene_ids_list)}_table.csv")
    if description_filter:
     df = df.loc[df['Product_Description'].str.lower().str.contains(description_filter.lower())]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(description_filter)}_table.csv")
    if symbol_filter:
     df = df.loc[df['Symbol'].str.lower().str.contains(symbol_filter.lower())]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(symbol_filter)}_table.csv")
    if truncation_type_filter:
      df = df.loc[df['Truncation_type'].str.lower().str.contains(truncation_type_filter.lower(),na=False)]
      csv_string = df.to_csv(index=False, encoding='utf-8')
      return dict(content=csv_string, filename=f"{(truncation_type_filter)}_table.csv")
    if MSE_cuttoff_filter:
     df = df.loc[df['MSE_cutoff'].str.lower().str.contains(MSE_cuttoff_filter.lower(),na=False)]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"{(MSE_cuttoff_filter)}_table.csv")
    if TTAA_filter_slider :
     if TTAA_filter_slider :
      df = df.loc[(df['TTAA'] >= TTAA_filter_slider[0]) & (df['TTAA'] <= TTAA_filter_slider[1])]
      csv_string = df.to_csv(index=False, encoding='utf-8')
      return dict(content=csv_string, filename=f"TTAA_range_{TTAA_filter_slider[0]}_{TTAA_filter_slider[1]}_table.csv")
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
   
    if cp_filter:
     df = df.loc[(df['cp'] >= cp_filter[0]) & (df['cp'] <= cp_filter[1])]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"cp_range_{cp_filter[0]}_{cp_filter[1]}_table.csv")
    if MSE_filter:
     df = df.loc[(df['MSE'] >= MSE_filter[0]) & (df['MSE'] <= MSE_filter[1])]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"MSE_range_{MSE_filter[0]}_{MSE_filter[1]}_table.csv")
    if R_i_filter:
     df = df.loc[(df['R_i'] >= R_i_filter[0]) & (df['R_i'] <= R_i_filter[1])]
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"R_i_range_{R_i_filter[0]}_{R_i_filter[1]}_table.csv")
    else:
     csv_string = df.to_csv(index=False, encoding='utf-8')
     return dict(content=csv_string, filename=f"datatable.csv")

@app.callback(
    Output('upload-modal-trunc', 'is_open'),
    [Input('open-modal-button-trunc', 'n_clicks'),Input('upload-modal-button-trunc', 'n_clicks'),],
    [State('upload-modal-trunc', 'is_open')]
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
    Output('gene-list-store-trunc','data'),
    Input('upload-gene-list-trunc', 'contents'),
    State('upload-gene-list-trunc', 'filename'),
    Input('copy-paste-gene-list-trunc', 'value'),
    Input('upload-modal-button-trunc', 'n_clicks'), 
    Input('clear-button-trunc', 'n_clicks'), 
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
    Output('clear-button-trunc', 'n_clicks'),
    Input('upload-modal-button-trunc', 'n_clicks'), 
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
   Output('copy-paste-gene-lis-trunc', 'value'),
   Input('clear-button-trunc', 'n_clicks'),
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
    Output('scatter-plot-trunc', 'figure'),
    Input('selected-network-nodes-trunc', 'data'),
    Input('network-nodes-table-trunc', 'children')
)
def update_scatter_plot(selected_cells,table):
    # Convert input geneids to a list
    if selected_cells:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
    #  geneid_list = [geneid.strip() for geneid in gene_name.split(',')]
    # else:
    #     geneid_list = []

    # Define colors based on whether the gene is in the geneid_list
     td.s_states2['color'] = td.s_states2['GeneID'].apply(lambda x: 'red' if x in gene_name else 'grey')

     fig = px.scatter(
        td.s_states2,
        x='R_i',
        y='min.val',
        color='color',
        hover_data={'GeneID': True,'color':False},
        color_discrete_map={'red': 'red', 'grey': 'grey'},
        labels={'log2(Total.CDS.length)': 'log2(CDS.length)', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
        title=''
    )

    #  fig.add_hline(y=0.3, line_width=5, line_dash="dash", line_color="yellow", layer="above")
    #  fig.add_hline(y=0.09, line_width=5, line_dash="dash", line_color="black", layer="above")

    #  fig.add_vline(x=0.1, line_width=5, line_dash="dash", line_color="red", layer="above")
    #  fig.add_vline(x=0.9, line_width=5, line_dash="dash", line_color="red", layer="above")

     fig.update_layout(
        template='simple_white',
        # title={
        #     'text': 'F2S Plot',
        #     'x': 0.4,
        #     'xanchor': 'center'
        # },
        xaxis_title='Normalized CDS',
        yaxis_title='Mean squared error',
        coloraxis_showscale=False,
        legend=dict(title=None),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # plot_bgcolor='white',
            width=500, 
            height=550
    )

     fig.update_traces(
        marker=dict(
            size=8,
            line=dict(width=1, color='black')
        )
    )
     for trace in fig.data:
      if trace.name == 'grey':
        trace.showlegend = False
      elif trace.name == 'red':
        trace.marker.size = 10  # Make red dots larger
        trace.name = gene_name  # Update legend label
    else: 
     fig = td.fig

    return fig    

@app.callback(
    Output('scatter-plot-trunc_5p', 'figure'),
    Input('selected-network-nodes-trunc', 'data'),
    Input('network-nodes-table-trunc', 'children')
)
def update_scatter_plot(selected_cells,table):
    # Convert input geneids to a list
    if selected_cells:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
    #  geneid_list = [geneid.strip() for geneid in gene_name.split(',')]
    # else:
    #     geneid_list = []

    # Define colors based on whether the gene is in the geneid_list
     td.s_states2_5p['color'] = td.s_states2_5p['GeneID'].apply(lambda x: 'red' if x in gene_name else 'grey')

     fig = px.scatter(
        td.s_states2_5p,
        x='R_i',
        y='min.val',
        color='color',
        hover_data={'GeneID': True,'color':False},
        color_discrete_map={'red': 'red', 'grey': 'grey'},
        labels={'log2(Total.CDS.length)': 'log2(CDS.length)', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
        title=''
    )

    #  fig.add_hline(y=0.3, line_width=5, line_dash="dash", line_color="yellow", layer="above")
    #  fig.add_hline(y=0.09, line_width=5, line_dash="dash", line_color="black", layer="above")

    #  fig.add_vline(x=0.1, line_width=5, line_dash="dash", line_color="red", layer="above")
    #  fig.add_vline(x=0.9, line_width=5, line_dash="dash", line_color="red", layer="above")

     fig.update_layout(
        template='simple_white',
        # title={
        #     'text': 'F2S Plot',
        #     'x': 0.4,
        #     'xanchor': 'center'
        # },
        xaxis_title='Normalized CDS',
        yaxis_title='Mean squared error',
        coloraxis_showscale=False,
        legend=dict(title=None),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # plot_bgcolor='white',
            width=500, 
            height=550
    )

     fig.update_traces(
        marker=dict(
            size=8,
            line=dict(width=1, color='black')
        )
    )
     for trace in fig.data:
      if trace.name == 'grey':
        trace.showlegend = False
      elif trace.name == 'red':
        trace.marker.size = 10  # Make red dots larger
        trace.name = gene_name  # Update legend label
    else: 
     fig = td.fig_5p

    return fig    


@app.callback(
    Output('scatter-plot-trunc_HMS', 'figure'),
    Input('selected-network-nodes-trunc', 'data'),
    Input('network-nodes-table-trunc', 'children')
)
def update_scatter_plot(selected_cells,table):
    # Convert input geneids to a list
    if selected_cells:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
    #  geneid_list = [geneid.strip() for geneid in gene_name.split(',')]
    # else:
    #     geneid_list = []

    # Define colors based on whether the gene is in the geneid_list
     td.s_states2['color'] = td.s_states2['GeneID'].apply(lambda x: 'red' if x in gene_name else 'grey')

     fig = px.scatter(
        td.s_states2,
        x='R_i',
        y='min.val',
        color='color',
        hover_data={'GeneID': True,'color':False},
        color_discrete_map={'red': 'red', 'grey': 'grey'},
        labels={'HMS': 'HMS', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
        title=''
    )

    #  fig.add_hline(y=0.3, line_width=5, line_dash="dash", line_color="yellow", layer="above")
    #  fig.add_hline(y=0.09, line_width=5, line_dash="dash", line_color="black", layer="above")

    #  fig.add_vline(x=0.1, line_width=5, line_dash="dash", line_color="red", layer="above")
    #  fig.add_vline(x=0.9, line_width=5, line_dash="dash", line_color="red", layer="above")

     fig.update_layout(
        template='simple_white',
        # title={
        #     'text': 'F2S Plot',
        #     'x': 0.4,
        #     'xanchor': 'center'
        # },
        xaxis_title='Normalized CDS',
        yaxis_title='Mean squared error',
        coloraxis_showscale=False,
        legend=dict(title=None),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # plot_bgcolor='white',
            width=500, 
            height=550
    )

     fig.update_traces(
        marker=dict(
            size=8,
            line=dict(width=1, color='black')
        )
    )
     for trace in fig.data:
      if trace.name == 'grey':
        trace.showlegend = False
      elif trace.name == 'red':
        trace.marker.size = 10  # Make red dots larger
        trace.name = gene_name  # Update legend label
    else: 
     fig = td.fig_HMS

    return fig    

@app.callback(
    Output('scatter-plot-trunc_5p_HMS', 'figure'),
    Input('selected-network-nodes-trunc', 'data'),
    Input('network-nodes-table-trunc', 'children')
)
def update_scatter_plot(selected_cells,table):
    # Convert input geneids to a list
    if selected_cells:
     selected_index = selected_cells[0]
     row = table[0]['props']['children'][selected_index]['props']['children']
     gene = row[0]
     gene_name = gene['props']['children']
    #  geneid_list = [geneid.strip() for geneid in gene_name.split(',')]
    # else:
    #     geneid_list = []

    # Define colors based on whether the gene is in the geneid_list
     td.s_states2_5p['color'] = td.s_states2_5p['GeneID'].apply(lambda x: 'red' if x in gene_name else 'grey')

     fig = px.scatter(
        td.s_states2_5p,
        x='R_i',
        y='min.val',
        color='color',
        hover_data={'GeneID': True,'color':False},
        color_discrete_map={'red': 'red', 'grey': 'grey'},
        labels={'HMS': 'HMS', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
        title=''
    )

    #  fig.add_hline(y=0.3, line_width=5, line_dash="dash", line_color="yellow", layer="above")
    #  fig.add_hline(y=0.09, line_width=5, line_dash="dash", line_color="black", layer="above")

    #  fig.add_vline(x=0.1, line_width=5, line_dash="dash", line_color="red", layer="above")
    #  fig.add_vline(x=0.9, line_width=5, line_dash="dash", line_color="red", layer="above")

     fig.update_layout(
        template='simple_white',
        # title={
        #     'text': 'F2S Plot',
        #     'x': 0.4,
        #     'xanchor': 'center'
        # },
        xaxis_title='Normalized CDS',
        yaxis_title='Mean squared error',
        coloraxis_showscale=False,
        legend=dict(title=None),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # plot_bgcolor='white',
            width=500, 
            height=550
    )

     fig.update_traces(
        marker=dict(
            size=8,
            line=dict(width=1, color='black')
        )
    )
     for trace in fig.data:
      if trace.name == 'grey':
        trace.showlegend = False
      elif trace.name == 'red':
        trace.marker.size = 10  # Make red dots larger
        trace.name = gene_name  # Update legend label
    else: 
     fig = td.fig_5p_HMS

    return fig    
