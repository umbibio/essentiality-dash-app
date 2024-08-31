from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

# Define a variable 'menu' which is currently set to None

menu = None
# Define the layout of the body using Dash Bootstrap Components
body = [
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H2("Plasmodium Knowlesi Essentiality Database")),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown('''
The Plasmodium knowlesi Essentiality Database provides an interactive app to explore gene essentiality, fitness and pertubation during the intra-erythrocytic development cycle of Plasmodium knowlesi.
To explore the data, click on one of the tabs above.

1. Essentiality: To explore the essentiality of protein-coding genes as well as identified lncRNAs based on different mathematical models (MIS, OIS, HMS). IGV spot check is allowed for any selection.
2. Perturbation: To explore the change of essentiality of Plasmodium knowlesi genes under DHA and GNF179 drug treatments.  
3. Fitness: To explore the fitness of the protein-coding genes.                                                                               
4. Truncation: To explore the truncatable genes.

''')),
])),
        ],),
    ), class_name="mb-4 mt-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Citation")),
            dbc.CardBody(dcc.Markdown('''
Brendan Elsworth, Sida Ye, Sheena Dass et al., "The essential genome of Plasmodium knowlesi reveals determinants of antimalarial susceptibility".
''')),
        ],),),
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Contact")),
            dbc.CardBody(dcc.Markdown('''
For questions or comments please contact:

mduraisi at hsph dot harvard dot edu​
                                      
kourosh dot zarringhalam at umb dot edu​
''')),],),),
    ]),
]
