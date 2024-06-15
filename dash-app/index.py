from dash import Dash, dcc,html
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State,MATCH
import plotly.graph_objs as go
import numpy as np
from app import app, server, url_base_pathname
import pages
from importlib import import_module
import re

# Get the list of page modules and sort them
page_modules = [mod for mod in pages.__loader__.get_resource_reader(pages.__name__).contents() if re.match('^p\d\d_', mod)]
page_modules.sort()
# Extract page names and corresponding hrefs
page_names = [re.sub('^p\d\d_', '', mod) for mod in page_modules]
page_hrefs = page_names.copy()
page_hrefs[0] = ''

# Create a list of dictionaries containing page information
page_info_list = [
    {
        'title': ' '.join([n for n in name.split('_')]),
        'module': module,
        'href': f'{url_base_pathname}{href}',
    }
    for name, module, href in zip(page_names, page_modules, page_hrefs)
]
# Import each page module
for page in page_info_list:
    import_module(f"pages.{page['module']}")

# Create navigation links based on page information
nav = dbc.Nav([
    dbc.NavItem(dbc.NavLink(page['title'], href=page['href'], id={'type': 'navlink', 'page': page['module']}))
    for page in page_info_list ], pills=True,style={'fontWeight': 'bold', 'fontSize': 20},)
#Create a logo using the app's asset
logo = html.Img(src=app.get_asset_url('logo_sida.png'), className="img-fluid")
#  set up the overall layout
app.layout = dbc.Container(
    dbc.Row([
        dcc.Location(id='url', refresh=False),
        # html.Datalist(id='list-suggested-gene-ids', children=[html.Option(value=word) for word in descriptions.ID]),
        # dcc.Store(id='expression-color-scale-store', storage_type='local'),
        dbc.Col([
          dbc.Row([
              dbc.Col(logo, width=3),
              dbc.Col([
                  html.Br(),
                  html.Br(),
                  html.H1([html.Span("P", style={'color': 'red'}),html.Span("lasmodium "),html.Span("K", style={'color': 'red'}),html.Span("nowlesi "),html.Span("E", style={'color': 'red'}),html.Span("ssentiality "),html.Span("D", style={'color': 'red'}),html.Span("atabase")],style={'fontFamily': 'Arial', 'fontWeight': 'bold', 'fontSize': 30})], width=9),]),
            dbc.Row(dbc.Col(id='left-menu')),
        ], width=10),
        html.Hr(),
        dbc.Col([
            dbc.Row(dbc.Col(nav), class_name="p-2"),
            dbc.Row(dbc.Col(id='page-content'), class_name='mt-4'),
        ], width=12),
    ], class_name="mt-4"),
    fluid=False
)

@app.callback(
    Output({'type': 'navlink', 'page': MATCH}, 'active'),
    Input('url', 'pathname'),
    State({'type': 'navlink', 'page': MATCH}, 'href'),)
def update_active_menu(pathname, page_href):
    """
    Update the active menu link based on the current URL pathname.

    Parameters:
        - pathname (str): The current URL pathname.
        - page_href (str): The href of the menu link being considered.

    Returns:
        - bool: True if the link is active, False otherwise.
    """
    return pathname == page_href


@app.callback(Output('left-menu', 'children'),
              Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """
    Display the content and menu of the selected page.

    Parameters:
        - pathname (str): The current URL pathname.

    Returns:
        - children (tuple): The left-menu and page-content components.
    """
    print(f"display page: {pathname}", flush=True)

    for page in page_info_list:
        if pathname == page['href']:

            page_app = getattr(pages, page['module'])
            menu = getattr(page_app, 'menu')
            body = getattr(page_app, 'body')

            return menu, body

    print(f"page not found: {pathname}", flush=True)
    return None, None

# Entry point for running the app
# if __name__ == '__main__':
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument('--host', type=str, default='127.0.0.1')
#     parser.add_argument('--port', type=int, default=8080)
#     parser.add_argument('--debug', action='store_true')
    
#     kvargs = vars(parser.parse_args())

#  # Run the Dash app with specified arguments
#     app.run_server(**kvargs)

if __name__ == '__main__':
     app.run(debug=True)