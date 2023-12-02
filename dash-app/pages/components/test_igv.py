from dash import Dash, html, dcc, callback, Input, Output, State,ALL,MATCH
import plotly.graph_objs as go
import dash_bio as dashbio
import plotly.express as px
from dash import callback_context 
from pages.components.data_loader import load_data,genome_data,genome
from app import app 
import pandas as pd
import os
import base64
import io
import numpy as np
import json
from dash.exceptions import PreventUpdate

path_mis = 'assets/MIS_sorted.xlsx'
path_ois = 'assets/OIS_sorted.xlsx'
path_hms = 'assets/HMS_sorted.xlsx'
path= 'assets/MIS_OIS_HMS_Pk_Pf_Pb_table_V3_OISMMISlike_rounded.xlsx'

path_bed = r'assets/Pk_5502transcript_modified.bed'
gene_to_genome = genome_data(path_bed)
genome_list = genome(gene_to_genome)
 
df_MIS = load_data(path_mis)
df_OIS = load_data(path_ois)
df_HMS = load_data(path_hms)
data = load_data(path)

tracks =[
                {
                    'name': 'TTAA Track',
                    'url': app.get_asset_url('75Pk_20231022_TTAA.sorted.bam'),
                    'indexURL': app.get_asset_url('75Pk_20231022_TTAA.sorted.bai'),
                    'displayMode': 'EXPANDED',
                    'nameField': 'gene',
                    'height': 150,
                    'color': 'rgb(169,169,169)'
                },
                {
                    'name': 'GTF track',
                    'url': app.get_asset_url('PlasmoDB-58_PknowlesiH.gtf'),
                    'displayMode': 'EXPANDED',
                    'height': 100,
                    'color': 'rgb(0,0,255)'
                },
                {
                    'name': 'TTAA Genome Pos',
                    'url': app.get_asset_url('Pk_theo_TTAA__include_contigs_R_modified_final2.bed'),
                    'displayMode': 'COLLAPSED',
                    'height': 100,
                    'color': 'rgb(255,0,0)'
                },
            ]