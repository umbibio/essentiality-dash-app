import pandas as pd
import numpy as np
from app import app 
import plotly.express as px
import re
import plotly.graph_objects as go
import statsmodels.api as sm


kneepoints1 = 0.26 
kneepoints2 = 0.88
df2 = pd.read_excel('assets/HMS_MFS_regression_trending_results_pcgenes_loess_normalization.xlsx')

# Positive: fitness favored genes
c1_Fslope_ep = df2[(df2['e.pvalue'] <= 0.05) & (df2['MFS.slope'] > 0)]['MFS.slope'].min()

# Negative: fitness defective genes
c2_Fslope_ep = df2[(df2['e.pvalue'] <= 0.05) & (df2['MFS.slope'] < 0)]['MFS.slope'].max()

# Filter for fitness_favored
fitness_favored = df2[
    (df2['MFS.slope'] > c1_Fslope_ep) &
    (df2['lm.adjusted.p.value'] <= 0.05) &
    (df2['Theo.num.unique.insertions'] >= 5) &
    (df2['HMS'] > 0.26)
]

# Filter for slow
slow = df2[
    (df2['MFS.slope'] < c2_Fslope_ep) &
    (df2['lm.adjusted.p.value'] <= 0.05) &
    (df2['Theo.num.unique.insertions'] >= 5) &
    (df2['HMS'] > 0.26)
]


# Create scatter plot
fig = go.Figure()

# Add scatter trace for the main dataset with grey points
fig.add_trace(go.Scatter(
    x=df2['HMS'], 
    y=df2['MFS.slope'], 
    mode='markers', 
    marker=dict(
        color='grey',  # Change color to grey
        opacity=0.5,
        size=10,
    ),
    hoverinfo='text',
    text=df2['geneID']+'<br>' +  
         'HMS: ' + df2['HMS'].astype(str) + '<br>' +  
         'MFS Slope: ' + df2['MFS.slope'].astype(str),
    showlegend=False,
))

# Add scatter trace for slow genes
fig.add_trace(go.Scatter(
    x=slow['HMS'], 
    y=slow['MFS.slope'],
    mode='markers', 
    marker=dict(color='#E3770C', size=10),
    name='Low Fitness',
    hoverinfo='text', 
    text=slow['geneID'] + '<br>' +  
         'HMS: ' + slow['HMS'].astype(str) + '<br>' +  
         'MFS Slope: ' + slow['MFS.slope'].astype(str)
))

# Add scatter trace for fitness favored genes
fig.add_trace(go.Scatter(
    x=fitness_favored['HMS'], 
    y=fitness_favored['MFS.slope'],
    mode='markers', 
    marker=dict(color='pink', size=10),
    name='High Fitness',
    hoverinfo='text',  
    text=fitness_favored['geneID'] + '<br>' +  
         'HMS: ' + fitness_favored['HMS'].astype(str) + '<br>' +  
         'MFS Slope: ' + fitness_favored['MFS.slope'].astype(str)
))

# Add vertical lines (vlines)
fig.add_vline(x=kneepoints1, line=dict(dash='dash', color='#C63135', width=2))
fig.add_vline(x=kneepoints2, line=dict(dash='dash', color='#237AB6', width=2))

# Add horizontal line (hline)
fig.add_hline(y=0, line=dict(dash='dash', color='black', width=1))

# Update layout
fig.update_layout(
    template='plotly_white',
    xaxis_title='HMS',
    yaxis_title='Fitness Index Score',
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),  # Update legend font size
        x=0.6, y=0.4
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    font=dict(color='black', size=18),  # Update axis and label font properties
    yaxis=dict(tickfont=dict(color='black'))
)

# Update y-axis range
fig.update_yaxes(range=[-1, 0.5])

# Remove grid lines
fig.update_layout(
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    showlegend=True
)



combined_data = pd.read_excel('assets/MFS_scores_results_pcgenes_loess_normalization.xlsx')
regression_results = pd.read_excel('assets/MFS_regression_trending_results_pcgenes_loess_normalization.xlsx')
regression_results2 = regression_results.copy()
regression_results2 = regression_results2.reset_index(drop=True) 
regression_results2['adjusted.p.value'] = regression_results2['adjusted.p.value'].apply(lambda x: '<0.001' if x < 0.001 else round(x, 3))

max_MFS = combined_data['Value'].max()
min_MFS = regression_results2['MFS_bottom_line'].min()
Input_gene_list =  ["PKNH_0503200", "PKNH_0000200", "PKNH_0000700"]

def trendingPlot(input_gene_list):
    figures = []
    for geneName in input_gene_list:
        # Input_gene_list1 = [gene for gene in Input_gene_list if gene == geneName]
        selected_df = combined_data[combined_data['geneID'] == geneName]
        # regression_results3 = regression_results2[regression_results2['geneID'] == geneName]
        regression_results_df = regression_results2[(regression_results2['geneID'] == geneName) & (regression_results2['term'] == "Timepoint")]
        selected_df['Timepoint'] = pd.Categorical(selected_df['Timepoint'], categories=selected_df['Timepoint'].unique(),ordered=False)

        # Create scatter plot
        fig2 = px.scatter(selected_df, x='Timepoint', y='Value', color='TPN',
                        title=f"{geneName}",
                        labels={'Timepoint': 'Timepoint', 'Value': 'MFS', 'TPN': 'TPN'})
        
        # Fit linear model and add regression line
        X = sm.add_constant(selected_df['Timepoint'].astype(float))
        model = sm.OLS(selected_df['Value'], X).fit()
        pred = model.predict(X)
        fig2.add_trace(go.Scatter(x=selected_df['Timepoint'], y=pred, mode='lines', line=dict(color='black'), name='Linear Fit'))

        # Add annotation
        annotation_text = f"adjusted p-value: {regression_results_df['adjusted.p.value'].values[0]}\nFIS: {round(regression_results_df['MFS.slope'].values[0], 3)}"
        fig2.add_annotation(
            text=annotation_text,
            xref="paper", yref="paper",
            x=1, y=1,
            showarrow=False,
            align='right',
            font=dict(size=12, color="black"),
            # bordercolor="black", borderwidth=1
        )

        # Add horizontal line
        fig2.add_hline(y=regression_results_df['MFS_bottom_line'].values[0], line=dict(dash='dash', color='black', width=1.2))

        # Set y-axis limits
        fig2.update_yaxes(range=[min_MFS, max_MFS])

        # Customize layout
        fig2.update_layout(
            xaxis=dict(
                title="Timepoint",
                tickmode='array',
                tickvals=[1, 2, 3],
                ticktext=['t1', 't2', 't3']
            ),
            yaxis_title="MFS",
            title=dict(text=f"{geneName}", x=0.5),
            legend_title_text=None,
            font=dict(size=14)
        )
        figures.append(fig2)
    return figures