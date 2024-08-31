import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objs as go

s_states2 = pd.read_excel('assets/prime3truncatable_4021pcgenes.xlsx')

# Calculate the 75th percentile for the 'min.val' column
min_val_cutoff = s_states2['min.val'].quantile(0.50)

s_states2['log2_Total_CDS_length'] = s_states2['Total.CDS.length'].apply(lambda x: np.log2(x) if x > 0 else None)

midpoint = np.log2(3000) 
custom_color_scale = [
    [0, "red"],
    [0.5, "white"],
    [1, "blue"]
]

# Create the scatter plot using Plotly Express
fig = px.scatter(
    s_states2,
    x='R_i',
    y='min.val',
    color='log2_Total_CDS_length',
    color_continuous_scale=custom_color_scale,
    labels={'log2(Total.CDS.length)': 'log2(CDS.length)', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
    # title='F2S Plot'
)



# Add horizontal and vertical lines as traces
# fig.add_trace(go.Scatter(
#     x=[0.1, 0.1],
#     y=[0, 0.7],
#     mode='lines',
#     line=dict(color="red", dash="dash", width=5),
#     name='Vertical Line 0.1',
#     showlegend=False
# ))

# fig.add_trace(go.Scatter(
#     x=[0.9, 0.9],
#     y=[0, 0.7],
#     mode='lines',
#     line=dict(color="red", dash="dash", width=5),
#     name='Vertical Line 0.9',
#     showlegend=False
# ))

# fig.add_trace(go.Scatter(
#     x=[0, 1],
#     y=[0.3, 0.3],
#     mode='lines',
#     line=dict(color="orange", dash="dash", width=5),
#     name='Horizontal Line 0.3',
#     showlegend=False
# ))

# fig.add_trace(go.Scatter(
#     x=[0, 1],
#     y=[0.09, 0.09],
#     mode='lines',
#     line=dict(color="black", dash="dash", width=5),
#     name='Horizontal Line 0.09',
#     showlegend=False
# ))

# Customize the plot layout
fig.update_layout(
    template='simple_white',
    # title={
    #     'text': 'F2S Plot',
    #     'x': 0.4,  # Center title horizontally
    #     'xanchor': 'center'  # Anchor title to center
    # },
    xaxis_title='Normalized CDS',
    yaxis_title='Mean squared error',
    legend_title=dict(text='log2(CDS.length)'),
    coloraxis_colorbar=dict(
        title='log2(CDS.length)',
        ticktext=['8', '10', '12','14'],
        len=0.6
    ),
    xaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    yaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    # margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins if needed
    plot_bgcolor='white',  # Background color of the plot area
    # paper_bgcolor='white', # Background color of the entire figure
                       width=500, 
            height=550
)
fig.update_traces(
    marker=dict(
        size=8,  # Marker size
        line=dict(
            width=1,  # Border width
            color='black'  # Border color
        )  # Border color
    )
)
# fig.add_hline(y=0.3, line_width=5, line_dash="dash", line_color="orange", layer="above")
# fig.add_hline(y=0.09, line_width=5, line_dash="dash", line_color="black", layer="above")

# fig.add_vline(x=0.1, line_width=5, line_dash="dash", line_color="red", layer="above")
# fig.add_vline(x=0.9, line_width=5, line_dash="dash", line_color="red", layer="above")


s_states2_5p = pd.read_excel('assets/prime5truncatable_4021pcgenes.xlsx')

# Calculate the 75th percentile for the 'min.val' column
min_val_cutoff_5p = s_states2_5p['min.val'].quantile(0.50)

s_states2_5p['log2_Total_CDS_length'] = s_states2_5p['Total.CDS.length'].apply(lambda x: np.log2(x) if x > 0 else None)

midpoint_5p = np.log2(3000) 
custom_color_scale = [
    [0, "red"],
    [0.5, "white"],
    [1, "blue"]
]

# Create the scatter plot using Plotly Express
fig_5p = px.scatter(
    s_states2_5p,
    x='R_i',
    y='min.val',
    color='log2_Total_CDS_length',
    color_continuous_scale=custom_color_scale,
    labels={'log2(Total.CDS.length)': 'log2(CDS.length)', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
    # title='F2S Plot'
)

# Customize the plot layout
fig_5p.update_layout(
    template='simple_white',
    # title={
    #     'text': 'F2S Plot',
    #     'x': 0.4,  # Center title horizontally
    #     'xanchor': 'center'  # Anchor title to center
    # },
    xaxis_title='Normalized CDS',
    yaxis_title='Mean squared error',
    legend_title=dict(text='log2(CDS.length)'),
    coloraxis_colorbar=dict(
        title='log2(CDS.length)',
        ticktext=['8', '10', '12','14'],
        len=0.6
    ),
    xaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    yaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    # margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins if needed
    plot_bgcolor='white',  # Background color of the plot area
    # paper_bgcolor='white', # Background color of the entire figure
                  width=500, 
            height=550
)
fig_5p.update_traces(
    marker=dict(
        size=8,  # Marker size
        line=dict(
            width=1,  # Border width
            color='black'  # Border color
        )  # Border color
    )
)

# fig_5p.add_hline(y=0.3, line_width=5, line_dash="dash", line_color="orange", layer="above")
# fig.add_hline(y=0.09, line_width=5, line_dash="dash", line_color="black", layer="above")

# fig_5p.add_vline(x=0.1, line_width=5, line_dash="dash", line_color="red", layer="above")
# fig_5p.add_vline(x=0.9, line_width=5, line_dash="dash", line_color="red", layer="above")



fig_HMS = px.scatter(
    s_states2,
    x='R_i',
    y='min.val',
    color='HMS',
    color_continuous_scale=custom_color_scale,
    labels={'HMS': 'HMS', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
    # title='F2S Plot'
)
fig_HMS.update_layout(
    template='simple_white',
    # title={
    #     'text': 'F2S Plot',
    #     'x': 0.4,  # Center title horizontally
    #     'xanchor': 'center'  # Anchor title to center
    # },
    xaxis_title='Normalized CDS',
    yaxis_title='Mean squared error',
    legend_title=dict(text='HMS'),
    coloraxis_colorbar=dict(
        title='HMS',
       ticktext=['0.0', '0.5', '1.0',],
        len=0.6
    ),
    xaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    yaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    # margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins if needed
    plot_bgcolor='white',  # Background color of the plot area
    # paper_bgcolor='white', # Background color of the entire figure
                       width=500, 
            height=550
)
fig_HMS.update_traces(
    marker=dict(
        size=8,  # Marker size
        line=dict(
            width=1,  # Border width
            color='black'  # Border color
        )  # Border color
    )
)

fig_5p_HMS = px.scatter(
    s_states2_5p,
    x='R_i',
    y='min.val',
    color='HMS',
    color_continuous_scale=custom_color_scale,
    labels={'HMS': 'HMS', 'R_i': 'Normalized CDS', 'min.val': 'Mean squared error'},
    # title='F2S Plot'
)

# Customize the plot layout
fig_5p_HMS.update_layout(
    template='simple_white',
    # title={
    #     'text': 'F2S Plot',
    #     'x': 0.4,  # Center title horizontally
    #     'xanchor': 'center'  # Anchor title to center
    # },
    xaxis_title='Normalized CDS',
    yaxis_title='Mean squared error',
    legend_title=dict(text='HMS'),
    coloraxis_colorbar=dict(
        title='HMS',
        ticktext=['0.0', '0.5', '1.0',],
        len=0.6
    ),
    xaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    yaxis=dict(
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove zero line
    ),
    # margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins if needed
    plot_bgcolor='white',  # Background color of the plot area
    # paper_bgcolor='white', # Background color of the entire figure
                  width=500, 
            height=550
)
fig_5p_HMS.update_traces(
    marker=dict(
        size=8,  # Marker size
        line=dict(
            width=1,  # Border width
            color='black'  # Border color
        )  # Border color
    )
)