# from itertools import count
# import pandas as pd
# import numpy as np
# from app import app 
# import plotly.graph_objs as go
# import plotly.express as px
# from plotly.subplots import make_subplots
# import matplotlib.pyplot as plt
# from matplotlib.text import Annotation
# from matplotlib.patches import FancyBboxPatch
# from matplotlib.lines import Line2D
# from scipy.stats import gaussian_kde
# from plotnine import *
# import seaborn as sns



# setA = 'assets/VC_SetA_GNF_High_day15_VS_WT_SetA_day15.xlsx'
# setB='assets/VC_SetB_GNF_High_day15_VS_WT_SetB_day18.xlsx'
# # Step 1: Read Data
# setA_file = pd.read_excel('assets/VC_SetA_GNF_High_day15_VS_WT_SetA_day15.xlsx')
# setA_file = setA_file.iloc[:, [0, 1, 5]]
# setA_file.columns = ["geneID", "A_mean_FC_sites", "A_cv"]

# setB_file = pd.read_excel('assets/VC_SetB_GNF_High_day15_VS_WT_SetB_day18.xlsx')
# setB_file = setB_file.iloc[:, [0, 1, 5]]
# setB_file.columns = ["geneID", "B_mean_FC_sites", "B_cv"]

# # Inner Join
# tmp = pd.merge(setA_file, setB_file, on="geneID", how="inner").dropna()

# # Step 2: Read Additional Data Files and Merge
# # setA_file_index2 = pd.read_excel('assets/VC_SetA_GNF_High_day15_VS_WT_SetA_day15.xlsx')
# # setB_file_index2 = pd.read_excel('assets/VC_SetB_GNF_High_day15_VS_WT_SetB_day18.xlsx')


# setA_file2 = pd.read_excel('assets/VC_SetA_GNF_High_day15_VS_WT_SetA_day15.xlsx')
# setA_file2 = setA_file2.iloc[:, [0, 1, 7]]
# setA_file2.columns = ["geneID", "setA_log2FC_edgeR", "setA_minus_log10FDR"]

# setB_file2 = pd.read_excel('assets/VC_SetB_GNF_High_day15_VS_WT_SetB_day18.xlsx')
# setB_file2 = setB_file2.iloc[:, [0, 1, 7]]
# setB_file2.columns = ["geneID", "setB_log2FC_edgeR", "setB_minus_log10FDR"]

# tmp2 = pd.merge(setA_file2, setB_file2, on="geneID", how="inner").dropna()

# # Full Join
# tmp = pd.merge(tmp, tmp2, on="geneID", how="outer").dropna()

# # Step 4: Calculate Maximum log2FC
# tmp["max.log2FC.edgeR"] = np.where(abs(tmp["setA_log2FC_edgeR"]) > abs(tmp["setB_log2FC_edgeR"]), tmp["setA_log2FC_edgeR"], tmp["setB_log2FC_edgeR"])

# # Step 5: Calculate log2 Mean FC
# tmp["setA_log2_mean_FC_sites"] = np.log2(tmp["A_mean_FC_sites"].replace({np.nan: None}))
# tmp["setB_log2_mean_FC_sites"] = np.log2(tmp["B_mean_FC_sites"].replace({np.nan: None}))

# # Step 6: Calculate Midpoint and Quantiles
# mid_value = tmp["max.log2FC.edgeR"].mean()
# xintercept_cutoff = tmp["A_cv"].quantile([0.03, 0.97])
# yintercept_cutoff = tmp["B_cv"].quantile([0.03, 0.97])

# # Step 7: Filter Genes based on CV values
# up_gene = tmp[(tmp["A_cv"] >= xintercept_cutoff[0.97]) & (tmp["B_cv"] >= yintercept_cutoff[0.97])]
# down_gene = tmp[(tmp["A_cv"] <= xintercept_cutoff[0.03]) & (tmp["B_cv"] <= yintercept_cutoff[0.03])]

# # Step 8: Combine DataFrames
# up_down_gene_list = pd.concat([up_gene, down_gene], ignore_index=True)



# # plot 
# custom_breaks=(0.2,0.4,0.6,0.8)
# p=(ggplot(tmp, aes(x='A_cv', y='B_cv'))
#      + geom_point(aes(color='max.log2FC.edgeR'))
#      + geom_hline(yintercept=[float(yintercept_cutoff[0.03]), float(yintercept_cutoff[0.97])], linetype="dashed", color="red")
#      + geom_vline(xintercept=[float(xintercept_cutoff[0.03]), float(xintercept_cutoff[0.97])], linetype="dashed", color="red")
#      + scale_color_gradient2(midpoint = 0, low = "darkblue", mid = "white", high = "red") 
#      + theme_bw()
#      + theme(panel_grid=element_blank(), axis_title=element_text(size=16), axis_text=element_text(size=14))
#      + geom_density_2d( levels=custom_breaks)
# #    + geom_text(aes(label='geneID'),data=tmp[tmp['geneID'].isin(up_gene['geneID'])],
# #                        nudge_x=1, nudge_y=1,
# #                        color='red',
# #                        size=4,
# #                        )
# #                         + labs(x=f'{setA}_cv_inverse', y=f'{setB}_cv_inverse') 
# #                          + geom_text(aes(label='geneID'),data=tmp[tmp['geneID'].isin(down_gene['geneID'])],
# #                        nudge_x=-1, nudge_y=-1,
# #                        color='blue',
# #                        size=4,)
# #                         + labs(x=f'{setA}_cv_inverse', y=f'{setB}_cv_inverse') 
# )