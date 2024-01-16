from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

# Define a variable 'menu' which is currently set to None

menu = None
# Define the layout of the body using Dash Bootstrap Components
body = [
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H2("Plasmodium Essentiality Database")),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown('''
The Plasmodium Essentiality Database provides an interactive app to explore gene essentiality during the intra-erythrocytic development cycle from several Plasmodium species.
To explore the data, click on one of the tabs above.

1. Essentiality: To explore the essentiality of protein-coding genes as well as identified lncRNAs based on different mathematical models (MIS, OIS, HMS). IGV spot check is allowed for any selection.
2. Perturbation: To explore the change of essentiality of Plasmodium knowlesi genes under different perturbations.                                         

''')),
])),
        ],),
    ), class_name="mb-4 mt-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Citation")),
            dbc.CardBody(dcc.Markdown('''
High density transposon insertion mutagenesis in Plasmodium knowlesi reveals the essential genome and determinants of drug resistance.
''')),
        ],),),
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Contact")),
            dbc.CardBody(dcc.Markdown('''
For questions or comments please contact:

mduraisi at hsph dot harvard dotedu​
                                      
kourosh.zarringhalam at umb dot edu​
''')),],),),
    ]),
]