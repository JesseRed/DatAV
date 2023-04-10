import dash
from dash import dcc, html

dash.register_page(__name__)

layout = html.Div(
    [
        dcc.Markdown('# This will be the content of Page 3')
    ]
)



# content = html.Div(
#     children=[
#         html.H1("BIOMAG Antalyser"),
#         html.Div(id="page-content", className="content")
#     ]
# )

# column_dropdown = dcc.Dropdown(
#     id='column-dropdown',
#     options=[{'label': col, 'value': col} for col in df.columns],
#     value=df.columns[0]
# )
