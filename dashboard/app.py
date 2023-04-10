"""
This app creates an animated sidebar using the dbc.Nav component and some local
CSS. Each menu item has an icon, when the sidebar is collapsed the labels
disappear and only the icons remain. Visit www.fontawesome.com to find
alternative icons to suit your needs!
dcc.Location is used to track the current location, a callback uses the current
location to render the appropriate page content. The active prop of each
NavLink is set automatically according to the current pathname. To use this
feature you must install dash-bootstrap-components >= 0.11.0.
For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import os, chardet
from config import df, colors

print(dash.__version__)


# Initialize the Dash

app = dash.Dash(__name__, 
                use_pages=True, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP, 
                    dbc.icons.FONT_AWESOME
                    ])



sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=app.get_asset_url('logo.png'), className='logo', style={"width": "3rem"}),
                html.H2("DatAV", style={'color': colors['font1']}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Calendar"),
                    ],
                    href="/pg2",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-envelope-open-text me-2"),
                        html.Span("Messages"),
                    ],
                    href="/pg3",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-chart-simple me-2"),
                        html.Span("GLM"),
                    ],
                    href="/pg4",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

content = html.Div(
            [
                # content of each page
                dash.page_container    
            ],
            className='content',
            style={'background-color':colors['background-color']}
        )

app.layout = dbc.Container(
    [
        dcc.Location(id="url"), 
        sidebar,
        content,
        dcc.Store(id='data-store')
    ],
    fluid=True,
    style={'background-color':colors['background-color']}
)
from pages.pg4 import register_callbacks_pg4
from pages.pg1 import register_callbacks_pg1
register_callbacks_pg4(app)
register_callbacks_pg1(app)
if __name__ == "__main__":
    app.run_server(debug=True)

