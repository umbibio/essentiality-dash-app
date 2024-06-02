
from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.express as px
from app import app 
import pandas as pd
import os
import base64
import io
import numpy as np
import pages.components.pertutbation_data  as pdata
from dash.exceptions import PreventUpdate



@app.callback(
Output("trending-plot",'figure'),
[Input('gene-list-store_pr','data')]
)
def update_trending_plot(geneName):
    df_plot=pdata.trending_plot(pdata.GNF_megatable,geneName)
  
    # Create a line plot with points using Plotly Express
    fig = px.line(df_plot, x='Time', y='logFC_edgeR', color='cond', facet_col='geneID',
              color_discrete_sequence=px.colors.qualitative.Set1, markers=True)
    
# Update the layout
    fig.update_layout(
    yaxis_title="log2FC_edgeR",
    template='plotly_white',
   )  
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    # fig= (ggplot(df_plot, aes(x='Time', y='logFC_edgeR', group='cond', color='cond'))
    #   + geom_line(size=1)
    #   + geom_point(size=1)
    #   + theme_bw()
    #   + facet_wrap('~ geneID', scales='free')
    #   + theme(strip_background=element_rect(colour="black", fill="white", size=1))
    #   + labs(y='log2FC_edgeR')
    #   )
    return fig

@app.callback(
Output("trending-plot1",'figure'),
Input('gene-list-store_pr','data')
)
def update_trending_plot1(geneName):
    df_plot=pdata.trending_plot(pdata.GNF_megatable,geneName)
    # Create a line plot with points using Plotly Express
    fig = px.line(df_plot, x='Time', y='log2_mean_FC_sites', color='cond', facet_col='geneID',
              color_discrete_sequence=px.colors.qualitative.Set1, markers=True)
   
# Update the layout
    fig.update_layout(
    template='plotly_white',
   )  
# Update facet labels
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    # fig1= (ggplot(df_plot, aes(x='Time', y='log2_mean_FC_sites', group='cond', color='cond'))
    #   + geom_line(size=1)
    #   + geom_point(size=1)
    #   + theme_bw()
    #   + facet_wrap('~ geneID', scales='free')
    #   + theme(strip_background=element_rect(colour="black", fill="white", size=1))
    #   )
    return fig


@app.callback(
   Output('copy-paste-gene-list_pr', 'value'),
   Input('clear-button_pr', 'n_clicks'),
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
    Output('upload-modal_pr', 'is_open'),
    [Input('open-modal-button_pr', 'n_clicks'),Input('upload-modal-button_pr', 'n_clicks'),],
    [State('upload-modal_pr', 'is_open')]
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
    
    Output('gene-list-store_pr','data'),
    Input('upload-gene-list_pr', 'contents'),
    State('upload-gene-list_pr', 'filename'),
    Input('copy-paste-gene-list_pr', 'value'),
    Input('upload-modal-button_pr', 'n_clicks'), 
    Input('clear-button_pr', 'n_clicks'), 
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
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), observed=False)
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
           

            return filter_value.split(',')
            

        except Exception as e:
            
            return ''
    elif copy_paste_value and upload_clicks and not clear:
      
        return [value.strip() for value in copy_paste_value.split(",")]
        
    else:
        raise PreventUpdate 
    