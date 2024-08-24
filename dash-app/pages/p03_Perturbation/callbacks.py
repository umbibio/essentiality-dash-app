
from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.express as px
from app import app 
import pandas as pd
import os
import base64
import io
import numpy as np
import plotly.graph_objects as go
import pages.components.pertutbation_data  as pdata
from dash.exceptions import PreventUpdate


@app.callback(
Output("trending-plot",'figure'),
[Input('gene-list-store_pr','data')]
)
def update_trending_plot(geneName):
 if geneName:
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
 else: 
    fig = pdata.fig_tr_GNF   
 return fig

@app.callback(
Output("trending-plot1",'figure'),
Input('gene-list-store_pr','data')
)
def update_trending_plot1(geneName):
 if geneName:
    df_plot=pdata.trending_plot(pdata.GNF_megatable,geneName)
    # Create a line plot with points using Plotly Express
    fig = px.line(df_plot, x='Time', y='log2_mean_FC_sites', color='cond', facet_col='geneID',
              color_discrete_sequence=px.colors.qualitative.Set1, markers=True,)
   
# Update the layout
    fig.update_layout(
    template='plotly_white',
   )  
# Update facet labels
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
 else: 
    fig = pdata.fig1_tr_GNF
 return fig



   
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
    elif clear :
       return ''    
    else:
        raise PreventUpdate 




@app.callback(
Output("trending-plot_DHA",'figure'),
[Input('gene-list-store_pr_DHA','data')]
)
def update_trending_plot_DHA(geneName):
 if geneName:
    df_plot=pdata.trending_plot_DHA(pdata.DHA_megatable,geneName)
  
    # Create a line plot with points using Plotly Express
    fig = px.line(df_plot, x='Time', y='logFC_edgeR', color='cond', facet_col='geneID',
              color_discrete_sequence=px.colors.qualitative.Set1, markers=True)
    
# Update the layout
    fig.update_layout(
    yaxis_title="log2FC_edgeR",
    template='plotly_white',
   )  
    fig.update_xaxes(categoryorder='array', categoryarray=sorted(df_plot['Time'].unique(), key=lambda x: int(pdata.extract_day(x))))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
 else : 
    fig=pdata.fig_tr_DHA
 return fig

@app.callback(
Output("trending-plot1_DHA",'figure'),
Input('gene-list-store_pr_DHA','data')
)
def update_trending_plot1_DHA(geneName):
 if geneName:
    df_plot=pdata.trending_plot_DHA(pdata.DHA_megatable,geneName)
    # Create a line plot with points using Plotly Express
    fig = px.line(df_plot, x='Time', y='log2_mean_FC_sites', color='cond', facet_col='geneID',
              color_discrete_sequence=px.colors.qualitative.Set1, markers=True)
   
# Update the layout
    fig.update_layout(
    template='plotly_white',
   )  
    fig.update_xaxes(categoryorder='array', categoryarray=sorted(df_plot['Time'].unique(), key=lambda x: int(pdata.extract_day(x))))
# Update facet labels
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
 else:
    fig=pdata.fig1_tr_DHA   
 return fig



@app.callback(
    Output('upload-modal_pr_DHA', 'is_open'),
    [Input('open-modal-button_pr_DHA', 'n_clicks'),Input('upload-modal-button_pr_DHA', 'n_clicks'),],
    [State('upload-modal_pr_DHA', 'is_open')]
)
def toggle_modal_DHA(open_clicks,upload_clicks,is_open):
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
    
    Output('gene-list-store_pr_DHA','data'),
    Input('upload-gene-list_pr_DHA', 'contents'),
    State('upload-gene-list_pr_DHA', 'filename'),
    Input('copy-paste-gene-list_pr_DHA', 'value'),
    Input('upload-modal-button_pr_DHA', 'n_clicks'), 
    Input('clear-button_pr_DHA', 'n_clicks'), 
    prevent_initial_call=True,
)
def update_manual_entry_from_upload_DHA(contents, filename, copy_paste_value, upload_clicks,clear):
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
    elif clear :
       return ''
        
    else:
        raise PreventUpdate 
    
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
   Output('copy-paste-gene-list_pr_DHA', 'value'),
   Input('clear-button_pr_DHA', 'n_clicks'),
)
def clear_list_DHA(n):
   """
    Callback to clear the copy-paste gene list input.

    Parameters:
        - n: Number of clicks on the 'Clear' button.

    Returns:
        str: Empty string to clear the input field.
    """
  
   if n :
      return ''
   

# @app.callback(
#     Output('clear-button_pr', 'n_clicks'),
#     Input('upload-modal-button_pr', 'n_clicks'), 
#     prevent_initial_call=True,  
# )
# def reset_n_clicks_pr(n):
#     """
#     Callback to reset the 'Clear' button clicks.

#     Parameters:
#         - n: Number of clicks on the upload modal button.

#     Returns:
#         None: Resets the 'Clear' button clicks.
#     """
#     return None

# @app.callback(
#     Output('clear-button_pr_DHA', 'n_clicks'),
#     Input('upload-modal-button_pr_DHA', 'n_clicks'), 
#     prevent_initial_call=True,  
# )
# def reset_n_clicks_DHA(n):
#     """
#     Callback to reset the 'Clear' button clicks.

#     Parameters:
#         - n: Number of clicks on the upload modal button.

#     Returns:
#         None: Resets the 'Clear' button clicks.
#     """
#     return None

# @app.callback(
#    Output('copy-paste-gene-list_pr_DHA', 'value'),
#    Input('clear-button_pr_DHA', 'n_clicks'),
# )
# def clear_list_pr(n):
#    """
#     Callback to clear the copy-paste gene list input.

#     Parameters:
#         - n: Number of clicks on the 'Clear' button.

#     Returns:
#         str: Empty string to clear the input field.
#     """
#    if n :
#       return ''
   
# @app.callback(
#    Output('copy-paste-gene-list_pr', 'value'),
#    Input('clear-button_pr', 'n_clicks'),
# )
# def clear_list_DHA(n):
#    """
#     Callback to clear the copy-paste gene list input.

#     Parameters:
#         - n: Number of clicks on the 'Clear' button.

#     Returns:
#         str: Empty string to clear the input field.
#     """
#    if n :
#       return ''

@app.callback(
    Output('scatter-plot1', 'figure'),
    Input('gene-list-store_pr','data')
)
def update_figure1(selected_genes):
 if selected_genes: 
   # Update color based on selected gene IDs
    pdata.tmp['color'] = [
        "darkblue" if x <= pdata.xintercept_cutoff_edgeR[0.02] and y <= pdata.yintercept_cutoff_edgeR[0.02] else  # below both lines
        "red" if x >= pdata.xintercept_cutoff_edgeR[0.98] and y >= pdata.yintercept_cutoff_edgeR[0.98] else  # above both lines
        "grey"  # in between the lines
        for x, y in zip(pdata.tmp['setA_log2FC_edgeR'], pdata.tmp['setB_log2FC_edgeR'])
    ]

    # Override color for selected genes
    pdata.tmp['color'] = [
        "green" if gene in selected_genes else color
        for gene, color in zip(pdata.tmp['geneID'], pdata.tmp['color'])
    ]
    
    # Create the updated plot
    fig = px.scatter(pdata.tmp, x='setA_log2FC_edgeR', y='setB_log2FC_edgeR', hover_data={'geneID':True , "color":False}, color='color',
                         color_discrete_map={"green": "green","darkblue": "darkblue", "red": "red", "grey": "grey"})
    
      # Add horizontal lines
    fig.add_hline(y=pdata.yintercept_cutoff_edgeR[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_hline(y=pdata.yintercept_cutoff_edgeR[0.98], line_width=3, line_dash="dash", line_color="purple")
       # Add vertical lines
    fig.add_vline(x=pdata.xintercept_cutoff_edgeR[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_vline(x=pdata.xintercept_cutoff_edgeR[0.98], line_width=3, line_dash="dash", line_color="purple")
    
    fig.update_layout(
        title_text='Gene level log2FC model by edgeR',
        title_x=0.5,
        xaxis_title='SetA_GNF_High_day15_edgeR_log2FC',
        yaxis_title='SetA_GNF_High_day15_edgeR_log2FC',
        legend=dict(
            title=None,
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        font={'color':"black"}
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(
                width=0.4,   # Border width
                color='black'  # Border color
            ),
        )
    )
    for trace in fig.data:
        if trace.name == 'green':
            trace.marker.size = 10  # Make green dots larger
            trace.name = ', '.join(selected_genes)  # Set the legend name to the selected genes
        else:
            trace.showlegend = False
 else:
    fig=pdata.fig1
    
 return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('gene-list-store_pr','data')
)
def update_figure(selected_genes):
    if selected_genes:
        # Separate data for selected and non-selected genes
        selected_data = pdata.tmp[pdata.tmp['geneID'].isin(selected_genes)]
        non_selected_data = pdata.tmp[~pdata.tmp['geneID'].isin(selected_genes)]

        # Create the figure
        fig = go.Figure()

        # Add scatter for selected genes (green)
        fig.add_trace(
            go.Scatter(
                x=selected_data['A_cv'],
                y=selected_data['B_cv'],
                mode='markers',
                marker=dict(color='green', size=10),
                name='Selected Genes',
                text = [
                    f"GeneID: {gene}<br>A_cv: {a_cv}<br>B_cv: {b_cv}<br>max.log2FC.edgeR: {log2fc}"
                    for gene, a_cv, b_cv, log2fc in zip(selected_data['geneID'], selected_data['A_cv'], selected_data['B_cv'], selected_data['max.log2FC.edgeR'])
                ],
                hoverinfo='text'
            )
        )

        # Add scatter for non-selected genes (using continuous color scale)
        fig.add_trace(
            go.Scatter(
                x=non_selected_data['A_cv'],
                y=non_selected_data['B_cv'],
                mode='markers',
                marker=dict(
                    color=non_selected_data['max.log2FC.edgeR'],  
                    colorscale=['darkblue', 'white', 'red'],
                    showscale=True
                ),
                name='Non-Selected Genes',
                text=[
                    f"GeneID: {gene}<br>A_cv: {a_cv}<br>B_cv: {b_cv}<br>max.log2FC.edgeR: {log2fc}"
                    for gene, a_cv, b_cv, log2fc in zip(non_selected_data['geneID'], non_selected_data['A_cv'], non_selected_data['B_cv'], non_selected_data['max.log2FC.edgeR'])
                ],
                hoverinfo='text'
            )
        )
    # Add horizontal lines
        fig.add_hline(y=pdata.yintercept_cutoff[0.03], line_width=3, line_dash="dash", line_color="red")
        fig.add_hline(y=pdata.yintercept_cutoff[0.97], line_width=3, line_dash="dash", line_color="red")

     # Add vertical lines
        fig.add_vline(x=pdata.xintercept_cutoff[0.03], line_width=3, line_dash="dash", line_color="red")
        fig.add_vline(x=pdata.xintercept_cutoff[0.97], line_width=3, line_dash="dash", line_color="red")

        fig.update_layout(
        title_text='CV inverse model',
        title_x=0.5,
        xaxis_title='SetA_GNF_High_day15_cv_inverse',
        yaxis_title='SetB_GNF_High_day15_inverse',
        # showlegend=False,
       legend=dict(
            title=None,
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        font={'color':"black"}
    )
    
        for trace in fig.data:
         if trace.name == 'Selected Genes':
            trace.marker.size = 10  # Make green dots larger
            trace.name = ', '.join(selected_genes)  # Set the legend name to the selected genes
         else:
            trace.showlegend = False
    else: 
     fig = pdata.fig
    
    return fig

@app.callback(
    Output('scatter-plot2', 'figure'),
    Input('gene-list-store_pr','data')
)
def update_figure2(selected_genes):
 if selected_genes:
    # Update color based on selected gene IDs
    pdata.tmp['color'] = [
        "darkblue" if x <= pdata.xintercept_cutoff_cv[0.02] and y <= pdata.yintercept_cutoff_cv[0.02] else  # below both lines
        "red" if x >= pdata.xintercept_cutoff_cv[0.98] and y >= pdata.yintercept_cutoff_cv[0.98] else  # above both lines
        "grey"  # in between the lines
        for x, y in zip(pdata.tmp['setA_log2_mean_FC_sites'], pdata.tmp['setB_log2_mean_FC_sites'])
    ]

    # Override color for selected genes
    pdata.tmp['color'] = [
        "green" if gene in selected_genes else color
        for gene, color in zip(pdata.tmp['geneID'], pdata.tmp['color'])
    ]
    # Create the updated plot
    fig = px.scatter(pdata.tmp, x='setA_log2_mean_FC_sites', y='setB_log2_mean_FC_sites', hover_data={'geneID':True , "color":False}, color='color',
                         color_discrete_map={"green": "green","darkblue": "darkblue", "red": "red", "grey": "grey"})
    
    fig.add_hline(y=pdata.yintercept_cutoff_cv[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_hline(y=pdata.yintercept_cutoff_cv[0.98], line_width=3, line_dash="dash", line_color="purple")
    # Add vertical lines
    fig.add_vline(x=pdata.xintercept_cutoff_cv[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_vline(x=pdata.xintercept_cutoff_cv[0.98], line_width=3, line_dash="dash", line_color="purple")
    
    fig.update_layout(
        title_text='Site level log2FC model',
        title_x=0.5,
        xaxis_title='SetA_GNF_High_day15_log2_mean_FC_sites',
        yaxis_title='SetA_GNF_High_day15_log2_mean_FC_sites',
         legend=dict(
            title=None,
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        font={'color':"black"}
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(
                width=0.4,   # Border width
                color='black'  # Border color
            ),
        )
    )
    for trace in fig.data:
        if trace.name == 'green':
            trace.marker.size = 10  # Make green dots larger
            trace.name = ', '.join(selected_genes)  # Set the legend name to the selected genes
        else:
            trace.showlegend = False
 else: 
    fig=pdata.fig2
    
 return fig



@app.callback(
    Output('scatter-plot1_DHA', 'figure'),
    Input('gene-list-store_pr_DHA','data')
)
def update_figure1_DHA(selected_genes):
 if selected_genes: 
   # Update color based on selected gene IDs
    pdata.tmp_DHA['color'] = [
        "darkblue" if x <= pdata.xintercept_cutoff_edgeR_DHA[0.02] and y <= pdata.yintercept_cutoff_edgeR_DHA[0.02] else  # below both lines
        "red" if x >= pdata.xintercept_cutoff_edgeR_DHA[0.98] and y >= pdata.yintercept_cutoff_edgeR_DHA[0.98] else  # above both lines
        "grey"  # in between the lines
        for x, y in zip(pdata.tmp_DHA['setA_log2FC_edgeR'], pdata.tmp_DHA['setB_log2FC_edgeR'])
    ]

    # Override color for selected genes
    pdata.tmp['color'] = [
        "green" if gene in selected_genes else color
        for gene, color in zip(pdata.tmp_DHA['geneID'], pdata.tmp_DHA['color'])
    ]
    
    # Create the updated plot
    fig = px.scatter(pdata.tmp_DHA, x='setA_log2FC_edgeR', y='setB_log2FC_edgeR', hover_data={'geneID':True , "color":False}, color='color',
                         color_discrete_map={"green": "green","darkblue": "darkblue", "red": "red", "grey": "grey"})
    
      # Add horizontal lines
    fig.add_hline(y=pdata.yintercept_cutoff_edgeR_DHA[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_hline(y=pdata.yintercept_cutoff_edgeR_DHA[0.98], line_width=3, line_dash="dash", line_color="purple")
       # Add vertical lines
    fig.add_vline(x=pdata.xintercept_cutoff_edgeR_DHA[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_vline(x=pdata.xintercept_cutoff_edgeR_DHA[0.98], line_width=3, line_dash="dash", line_color="purple")
    
    fig.update_layout(
        title_text='Gene level log2FC model by edgeR',
        title_x=0.5,
        xaxis_title='SetA_GNF_High_day15_edgeR_log2FC',
        yaxis_title='SetA_GNF_High_day15_edgeR_log2FC',
        legend=dict(
            title=None,
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        font={'color':"black"}
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(
                width=0.4,   # Border width
                color='black'  # Border color
            ),
        )
    )
    for trace in fig.data:
        if trace.name == 'green':
            trace.marker.size = 10  # Make green dots larger
            trace.name = ', '.join(selected_genes)  # Set the legend name to the selected genes
        else:
            trace.showlegend = False
 else:
    fig=pdata.fig1_DHA
    
 return fig

@app.callback(
    Output('scatter-plot_DHA', 'figure'),
    Input('gene-list-store_pr_DHA','data')
)
def update_figure_DHA(selected_genes):
    if selected_genes:
        # Separate data for selected and non-selected genes
        selected_data = pdata.tmp_DHA[pdata.tmp_DHA['geneID'].isin(selected_genes)]
        non_selected_data = pdata.tmp_DHA[~pdata.tmp_DHA['geneID'].isin(selected_genes)]

        # Create the figure
        fig = go.Figure()

        # Add scatter for selected genes (green)
        fig.add_trace(
            go.Scatter(
                x=selected_data['A_cv'],
                y=selected_data['B_cv'],
                mode='markers',
                marker=dict(color='green', size=10),
                name='Selected Genes',
                text = [
                    f"GeneID: {gene}<br>A_cv: {a_cv}<br>B_cv: {b_cv}<br>max.log2FC.edgeR: {log2fc}"
                    for gene, a_cv, b_cv, log2fc in zip(selected_data['geneID'], selected_data['A_cv'], selected_data['B_cv'], selected_data['max.log2FC.edgeR'])
                ],
                hoverinfo='text'
            )
        )

        # Add scatter for non-selected genes (using continuous color scale)
        fig.add_trace(
            go.Scatter(
                x=non_selected_data['A_cv'],
                y=non_selected_data['B_cv'],
                mode='markers',
                marker=dict(
                    color=non_selected_data['max.log2FC.edgeR'],  
                    colorscale=['darkblue', 'white', 'red'],
                    showscale=True
                ),
                name='Non-Selected Genes',
                text=[
                    f"GeneID: {gene}<br>A_cv: {a_cv}<br>B_cv: {b_cv}<br>max.log2FC.edgeR: {log2fc}"
                    for gene, a_cv, b_cv, log2fc in zip(non_selected_data['geneID'], non_selected_data['A_cv'], non_selected_data['B_cv'], non_selected_data['max.log2FC.edgeR'])
                ],
                hoverinfo='text'
            )
        )
    # Add horizontal lines
        fig.add_hline(y=pdata.yintercept_cutoff_DHA[0.03], line_width=3, line_dash="dash", line_color="red")
        fig.add_hline(y=pdata.yintercept_cutoff_DHA[0.97], line_width=3, line_dash="dash", line_color="red")

     # Add vertical lines
        fig.add_vline(x=pdata.xintercept_cutoff_DHA[0.03], line_width=3, line_dash="dash", line_color="red")
        fig.add_vline(x=pdata.xintercept_cutoff_DHA[0.97], line_width=3, line_dash="dash", line_color="red")

        fig.update_layout(
        title_text='CV inverse model',
        title_x=0.5,
        xaxis_title='SetA_GNF_High_day15_cv_inverse',
        yaxis_title='SetB_GNF_High_day15_inverse',
        # showlegend=False,
       legend=dict(
            title=None,
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        font={'color':"black"}
    )
    
        for trace in fig.data:
         if trace.name == 'Selected Genes':
            trace.marker.size = 10  # Make green dots larger
            trace.name = ', '.join(selected_genes)  # Set the legend name to the selected genes
         else:
            trace.showlegend = False
    else: 
     fig = pdata.fig_DHA
    
    return fig

@app.callback(
    Output('scatter-plot2_DHA', 'figure'),
    Input('gene-list-store_pr_DHA','data')
)
def update_figure2_DHA(selected_genes):
 if selected_genes:
    # Update color based on selected gene IDs
    pdata.tmp_DHA['color'] = [
        "darkblue" if x <= pdata.xintercept_cutoff_cv_DHA[0.02] and y <= pdata.yintercept_cutoff_cv_DHA[0.02] else  # below both lines
        "red" if x >= pdata.xintercept_cutoff_cv_DHA[0.98] and y >= pdata.yintercept_cutoff_cv_DHA[0.98] else  # above both lines
        "grey"  # in between the lines
        for x, y in zip(pdata.tmp_DHA['setA_log2_mean_FC_sites'], pdata.tmp_DHA['setB_log2_mean_FC_sites'])
    ]

    # Override color for selected genes
    pdata.tmp_DHA['color'] = [
        "green" if gene in selected_genes else color
        for gene, color in zip(pdata.tmp_DHA['geneID'], pdata.tmp_DHA['color'])
    ]
    # Create the updated plot
    fig = px.scatter(pdata.tmp_DHA, x='setA_log2_mean_FC_sites', y='setB_log2_mean_FC_sites', hover_data={'geneID':True , "color":False}, color='color',
                         color_discrete_map={"green": "green","darkblue": "darkblue", "red": "red", "grey": "grey"})
    
    fig.add_hline(y=pdata.yintercept_cutoff_cv_DHA[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_hline(y=pdata.yintercept_cutoff_cv_DHA[0.98], line_width=3, line_dash="dash", line_color="purple")
    # Add vertical lines
    fig.add_vline(x=pdata.xintercept_cutoff_cv_DHA[0.02], line_width=3, line_dash="dash", line_color="purple")
    fig.add_vline(x=pdata.xintercept_cutoff_cv_DHA[0.98], line_width=3, line_dash="dash", line_color="purple")
    
    fig.update_layout(
        title_text='Site level log2FC model',
        title_x=0.5,
        xaxis_title='SetA_GNF_High_day15_log2_mean_FC_sites',
        yaxis_title='SetA_GNF_High_day15_log2_mean_FC_sites',
         legend=dict(
            title=None,
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        font={'color':"black"}
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(
                width=0.4,   # Border width
                color='black'  # Border color
            ),
        )
    )
    for trace in fig.data:
        if trace.name == 'green':
            trace.marker.size = 10  # Make green dots larger
            trace.name = ', '.join(selected_genes)  # Set the legend name to the selected genes
        else:
            trace.showlegend = False
 else: 
    fig=pdata.fig2_DHA
    
 return fig


@app.callback(
    Output('download-data_pr', 'data'),
    Input('download-button_pr', 'n_clicks'),
    prevent_initial_call=True,
)
def update_download_button(n_clicks):
   if n_clicks is None:
      PreventUpdate
   if n_clicks is not None:
    df = pdata.GNF_megatable.copy() 
    csv_string = df.to_csv(index=False, encoding='utf-8')
    return dict(content=csv_string, filename=f"GNF_megatable.csv")
   
@app.callback(
    Output('download-data_pr_DHA', 'data'),
    Input('download-button_pr_DHA', 'n_clicks'),
    prevent_initial_call=True,
)
def update_download_button_DHA(n_clicks):
   if n_clicks is None:
      PreventUpdate
   if n_clicks is not None:
    df = pdata.DHA_megatable.copy() 
    csv_string = df.to_csv(index=False, encoding='utf-8')
    return dict(content=csv_string, filename=f"DHA_megatable.csv")
   
@app.callback(
    Output('download-button_pr', 'n_clicks'),
    Input('gene-list-store_pr','data'),
   Input('upload-modal-button_pr', 'n_clicks'),
    prevent_initial_call=True,
)
def update_download_button(n_clicks,list,modal):
       return None

@app.callback(
    Output('download-button_pr_DHA', 'n_clicks'),
    Input('gene-list-store_pr_DHA','data'),
   Input('upload-modal-button_pr_DHA', 'n_clicks'),
    prevent_initial_call=True,
)
def update_download_button(n_clicks,list,modal):
       return None