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
The Plasmodium Essentiality Database provides an interactive app to explore gene essentiality and fitness during the intra-erythrocytic development cycle from several Plasmodium species. 
To explore the data, click on one of the tabs above.

1. Essentiality: Explore the essentiality of genes based on different mathematical model (MIS, OIS, HMS).
2. Fitness: Explore the defective and advantageous fitness of the genes​.
3. Non-coding RNAs: Explore the essentiality of non-coding RNAs across the genome of Plasmodium knowlesi​.
4. Perturbation: Explore the essentiality of Plasmodium knowlesi genes under perturbation​.                                        

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