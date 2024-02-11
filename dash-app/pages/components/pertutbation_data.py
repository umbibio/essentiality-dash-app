from itertools import count
import pandas as pd
import numpy as np
from app import app 
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib.text import Annotation
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde
from plotnine import *
import seaborn as sns
from plotnine import ggplot, aes, geom_point
import re


setA = 'SetA_GNF_High_day15'
setB='SetB_GNF_High_day15'
# Step 1: Read Data
setA_file = pd.read_excel('assets/VC_SetA_GNF_High_day15_VS_WT_SetA_day15.xlsx')
setA_file = setA_file.iloc[:, [0, 1, 5]]
setA_file.columns = ["geneID", "A_mean_FC_sites", "A_cv"]

setB_file = pd.read_excel('assets/VC_SetB_GNF_High_day15_VS_WT_SetB_day18.xlsx')
setB_file = setB_file.iloc[:, [0, 1, 5]]
setB_file.columns = ["geneID", "B_mean_FC_sites", "B_cv"]

# Inner Join
tmp = pd.merge(setA_file, setB_file, on="geneID", how="inner").dropna()


setA_file2 = pd.read_excel('assets/DIG_SetA_GNF_High_day15_VS_WT_SetA_day15.xlsx')
setA_file2 = setA_file2.iloc[:, [0, 1, 7]]
setA_file2.columns = ["geneID", "setA_log2FC_edgeR", "setA_minus_log10FDR"]

setB_file2 = pd.read_excel('assets/DIG_SetB_GNF_High_day15_VS_WT_SetB_day18.xlsx')
setB_file2 = setB_file2.iloc[:, [0, 1, 7]]
setB_file2.columns = ["geneID", "setB_log2FC_edgeR", "setB_minus_log10FDR"]

tmp2 = pd.merge(setA_file2, setB_file2, on="geneID", how="inner")

# Full Join
tmp = pd.merge(tmp, tmp2, on="geneID", how="outer").dropna()

# Step 4: Calculate Maximum log2FC
tmp['max.log2FC.edgeR'] = tmp.apply(lambda row: row['setA_log2FC_edgeR'] if abs(row['setA_log2FC_edgeR']) > abs(row['setB_log2FC_edgeR']) else row['setB_log2FC_edgeR'], axis=1)
# Step 5: Calculate log2 Mean FC
tmp['setA_log2_mean_FC_sites'] = np.log2(tmp['A_mean_FC_sites'])
tmp['setB_log2_mean_FC_sites'] = np.log2(tmp['B_mean_FC_sites'])

# Step 6: Calculate Midpoint and Quantiles
mid_value = np.mean(tmp['max.log2FC.edgeR'])
xintercept_cutoff = tmp["A_cv"].quantile([0.03, 0.97])
yintercept_cutoff = tmp["B_cv"].quantile([0.03, 0.97])

# Step 7: Filter Genes based on CV values
up_gene = tmp[(tmp["A_cv"] >= xintercept_cutoff[0.97]) & (tmp["B_cv"] >= yintercept_cutoff[0.97])]
down_gene = tmp[(tmp["A_cv"] <= xintercept_cutoff[0.03]) & (tmp["B_cv"] <= yintercept_cutoff[0.03])]

# Add 'Change' column
up_gene['Change'] = 'Increase'
down_gene['Change'] = 'Decrease'

# Step 8: Combine DataFrames
up_down_gene_list = pd.concat([up_gene, down_gene], ignore_index=True)



# plot 
custom_breaks=(0.2,0.4,0.6,0.8)

# Create scatter plot
fig = px.scatter(tmp, x='A_cv', y='B_cv', color='max.log2FC.edgeR',
                 color_continuous_scale=['darkblue', 'white', 'red'], hover_data=['geneID'])

# Add horizontal lines
fig.add_hline(y=yintercept_cutoff[0.03], line_width=3, line_dash="dash", line_color="red")
fig.add_hline(y=yintercept_cutoff[0.97], line_width=3, line_dash="dash", line_color="red")

# Add vertical lines
fig.add_vline(x=xintercept_cutoff[0.03], line_width=3, line_dash="dash", line_color="red")
fig.add_vline(x=xintercept_cutoff[0.97], line_width=3, line_dash="dash", line_color="red")
# Add density contours
# fig.add_trace(go.Histogram2dContour(x=tmp['A_cv'], y=tmp['B_cv'], 
                                    
#                                       # Set opacity to 0 for no color fill
#                                     line=dict(color='grey'),  # Set contour line color to grey
#                                     contours=dict(start=0, end=custom_breaks[-1], size=len(custom_breaks))))

# Add text labels
# fig.add_trace(go.Scatter(x=tmp[tmp['geneID'].isin(up_gene['geneID'])]['A_cv'],
#                          y=tmp[tmp['geneID'].isin(up_gene['geneID'])]['B_cv'],
#                          mode='text',
#                          text=tmp[tmp['geneID'].isin(up_gene['geneID'])]['geneID'],
#                          textposition='bottom right',
#                          textfont=dict(color='red', size=8)))

# fig.add_trace(go.Scatter(x=tmp[tmp['geneID'].isin(down_gene['geneID'])]['A_cv'],
#                          y=tmp[tmp['geneID'].isin(down_gene['geneID'])]['B_cv'],
#                          mode='text',
#                          text=tmp[tmp['geneID'].isin(down_gene['geneID'])]['geneID'],
#                          textposition='top left',
#                          textfont=dict(color='blue', size=8)))
# Update layout
fig.update_layout(title_text=f'CV inverse model',
                   title_x=0.5,
                  xaxis_title=f'{setA}_cv_inverse', yaxis_title=f'{setB}_cv_inverse',
                  showlegend=False,
                  plot_bgcolor='white')



xintercept_cutoff_edgeR = tmp["setA_log2FC_edgeR"].quantile([0.02, 0.98])
yintercept_cutoff_edgeR= tmp["setB_log2FC_edgeR"].quantile([0.02, 0.98])




# Filter data based on quantiles
up_gene_edgeR = tmp[(tmp['setA_log2FC_edgeR'] >= xintercept_cutoff_edgeR[0.98]) & (tmp['setB_log2FC_edgeR'] >= yintercept_cutoff_edgeR[0.98])]

down_gene_edgeR =tmp[(tmp['setA_log2FC_edgeR'] >= xintercept_cutoff_edgeR[0.02]) & (tmp['setB_log2FC_edgeR'] >= yintercept_cutoff_edgeR[0.02])]

# Add 'Change' column
up_gene_edgeR['Change'] = 'Increase'
down_gene_edgeR['Change'] = 'Decrease'


# Step 8: Combine DataFrames
up_down_gene_list_edgeR = pd.concat([up_gene_edgeR, down_gene_edgeR], ignore_index=True)

tmp['color'] = [
    "darkblue" if x <= xintercept_cutoff_edgeR[0.02] and y <= yintercept_cutoff_edgeR[0.02] else  # below both lines
    "red" if x >= xintercept_cutoff_edgeR[0.98] and y >= yintercept_cutoff_edgeR[0.98] else  # above both lines
    "grey"  # in between the lines
    for x, y in zip(tmp['setA_log2FC_edgeR'], tmp['setB_log2FC_edgeR'])
]
fig1 = px.scatter(tmp, x='setA_log2FC_edgeR', y='setB_log2FC_edgeR', hover_data=['geneID'],color='color',color_discrete_map={"darkblue": "darkblue", "red": "red", "grey": "grey"}
                 )

# Add horizontal lines
fig1.add_hline(y=yintercept_cutoff_edgeR[0.02], line_width=3, line_dash="dash", line_color="purple")
fig1.add_hline(y=yintercept_cutoff_edgeR[0.98], line_width=3, line_dash="dash", line_color="purple")
# Add vertical lines
fig1.add_vline(x=xintercept_cutoff_edgeR[0.02], line_width=3, line_dash="dash", line_color="purple")
fig1.add_vline(x=xintercept_cutoff_edgeR[0.98], line_width=3, line_dash="dash", line_color="purple")
# Update layout
fig1.update_layout(title_text=f'Gene level log2FC model by edgeR',
                   title_x=0.5,
                  xaxis_title=f'{setA}_edgeR_log2FC', yaxis_title=f'{setB}_edgeR_log2FC',
                  showlegend=False,
                  plot_bgcolor='white')

xintercept_cutoff_cv = tmp["setA_log2_mean_FC_sites"].quantile([0.02, 0.98])
yintercept_cutoff_cv = tmp["setB_log2_mean_FC_sites"].quantile([0.02, 0.98])

# Filter data based on quantiles
up_gene_cv = tmp[(tmp['setA_log2_mean_FC_sites'] >= xintercept_cutoff_cv[0.98]) & (tmp['setB_log2_mean_FC_sites'] >= yintercept_cutoff_cv[0.98])]

down_gene_cv =tmp[(tmp['setA_log2_mean_FC_sites'] >= xintercept_cutoff_cv[0.02]) & (tmp['setB_log2_mean_FC_sites'] >= yintercept_cutoff_cv[0.02])]

# Add 'Change' column
up_gene_cv['Change'] = 'Increase'
down_gene_cv['Change'] = 'Decrease'


# Step 8: Combine DataFrames
up_down_gene_list_cv = pd.concat([up_gene_cv, down_gene_cv], ignore_index=True)


# Apply the function to create a 'color' column in your DataFrame

tmp['color'] = [
    "darkblue" if x <= xintercept_cutoff_cv[0.02] and y <= yintercept_cutoff_cv[0.02] else  # below both lines
    "red" if x >= xintercept_cutoff_cv[0.98] and y >= yintercept_cutoff_cv[0.98] else  # above both lines
    "grey"  # in between the lines
    for x, y in zip(tmp['setA_log2_mean_FC_sites'], tmp['setB_log2_mean_FC_sites'])
]

# Create scatter plot
fig2 = px.scatter(tmp, x='setA_log2_mean_FC_sites', y='setB_log2_mean_FC_sites',
                  hover_data=['geneID'], color='color',color_discrete_map={"darkblue": "darkblue", "red": "red", "grey": "grey"})

# Add horizontal lines
fig2.add_hline(y=yintercept_cutoff_cv[0.02], line_width=3, line_dash="dash", line_color="purple")
fig2.add_hline(y=yintercept_cutoff_cv[0.98], line_width=3, line_dash="dash", line_color="purple")
# Add vertical lines
fig2.add_vline(x=xintercept_cutoff_cv[0.02], line_width=3, line_dash="dash", line_color="purple")
fig2.add_vline(x=xintercept_cutoff_cv[0.98], line_width=3, line_dash="dash", line_color="purple")
# Update layout
fig2.update_layout(title_text=f'Site level log2FC model',
                   title_x=0.5,
                  xaxis_title=f'{setA}_log2_mean_FC_sites', yaxis_title=f'{setB}_log2_mean_FC_sites',
                  showlegend=False,
                  plot_bgcolor='white')


##Trending plot 

GNF_megatable = pd.read_excel('assets/GNF_megatable.xlsx')
DHA_megatable = pd.read_excel('assets/DHA_megatable.xlsx')
LF_megatable = pd.read_excel('assets/LF_megatable.xlsx')

def extract_day(time_str):
    return re.sub(r'day', '', time_str)

def trending_plot(Drug_megatable,geneName):
    # Filter the megatable to include only the specified genes
    megatable = Drug_megatable[Drug_megatable['geneID'].isin(geneName)]
    
    # Select columns containing "_logFC" in their names
    df = megatable.filter(like='_logFC')
    print(df.head(10))
    # Select columns containing "mean_log2_FC_sites" in their names
    df2 = megatable.filter(like='mean_log2_FC_sites')
    
    # Select columns containing "mean_FC_sites" in their names
    df3 = megatable.filter(like='mean_FC_sites')
    
    # Create a dataframe to plot
    df_plot = pd.DataFrame({
        'geneID': np.repeat(megatable['geneID'], df.shape[1]),
        'Time': np.tile(df.columns.str.split('_').str[-2], df.shape[0]),
        'cond': np.tile(df.columns.str.split('_day').str[0], df.shape[0]),
        'logFC_edgeR': df.values.flatten(),
        'mean_logFC_sites': df2.values.flatten(),
        'mean_FC_sites': df3.values.flatten()
    })
    
    # Calculate log2 mean_FC_sites
    df_plot['log2_mean_FC_sites'] = np.log2(df_plot['mean_FC_sites'])
    
    # Extract day number from the Time column
    df_plot['DayNumber'] = df_plot['Time'].apply(extract_day).astype(int)
    
    # Arrange the dataframe by geneID and DayNumber
    df_plot = df_plot.sort_values(by=['geneID', 'DayNumber'],ascending=[True, True])
    
    # Convert geneID, Time, and cond columns to categorical with unique levels
    df_plot['geneID'] = pd.Categorical(df_plot['geneID'], categories=df_plot['geneID'].unique())
    df_plot['Time'] = pd.Categorical(df_plot['Time'], categories=df_plot['Time'].unique())
    df_plot['cond'] = pd.Categorical(df_plot['cond'], categories=df_plot['cond'].unique())
    
    return df_plot
