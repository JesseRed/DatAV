import dash
from dash import dcc, html, Output, Input, State, dash_table
import plotly.express as px
from config import df, colors, df_org
import config
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import base64
import io
import datetime
import os, chardet, csv

dash.register_page(__name__, path='/')



layout = html.Div(
    children=[
        # Ueberschrift
        html.Div(
            children=[
                html.H1(
                    children="Options",
                    className = "page-title"
                ),
            ],
            className="mytitle",
        ),
        # main Content of the page
        html.Div(
            children = [
                html.Div(
                    id='pg1-subtitle',
                    children = '', 
                    style={
                        'whiteSpace': 'pre-line', 
                        'color': colors['font1'],
                        #'width': '140px',
                        'text-align': 'center',
                        }
                )
            ]
        ),
        html.Div([
            html.H2('File Browser for your csv File to be analysed'),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                    ]),
                    style={
                        'width': '50%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False
            )
        ]),
        html.Div(className='general-spacing'),
        html.Div([
            html.H2('Validation Datasets from Andy Field (Discovering Statistics using R)'),
            html.Button('Beer-googles', id='beer-googles-button', n_clicks=0, className='standard-button'),
            ],
            # style={
            #     'width': '100%',
            #     'height': '60px',
            #     'lineHeight': '60px',
            #     'borderWidth': '1px',
            #     'borderStyle': 'dashed',
            #     'borderRadius': '5px',
            #     'textAlign': 'center',
            #     'margin': '10px'
            # },
            # style={
            #     'background-color': colors['background-color'],
            #     'color': colors['font1'],
            #     'padding': '10px'
            # }
        ),
        html.Div(
            id='output-data-upload'
        ),
        html.Div(className='general-spacing'),
         # the Dataframe
        html.Div(
            children = [
            html.Details([
                html.Summary('Loaded Dataframe ... Click to expand', style={'background-color':colors['background-color']}),
                dash_table.DataTable(
                    id = 'pg1_datatable',
                    
                    style_table={
                        'width': '100%',
                    },
                    style_header={
                        'backgroundColor':'black',
                        'color': colors['font1'],
                        'fontWeight': 'bold'
                    }, 
                    style_data={
                        'color': colors['font1'],
                        'backgroundColor': colors['background-panel']
                    },
                                
                )
            ],
            )
            ],
            
        )
    ],
    style={
        'background-color': colors['background-color'],
        'color': colors['font1'],
        'padding': '10px'
    }

)

# def create_table(dfx):
#     dash_table.DataTable(
#         columns = [{"name": i, "id": i} for i in dfx.columns],
#         data = dfx.to_dict('records')
#     )
#     return dash_table

# Define the callback function that updates the output

def parse_contents(contents, filename):

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            #df = pd.read_csv(io.StringIO(decoded), sep = None, engine='python')
            #df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep = '|')
            result = chardet.detect(decoded)
            dialect = csv.Sniffer().sniff(io.StringIO(decoded.decode(result['encoding'])).read(1024))
            #print(f'The delimiter in the CSV file is "{delimiter}"')
            df = pd.read_csv(io.StringIO(decoded.decode(result['encoding'])), sep = dialect.delimiter, engine='python')
        
            # df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ]), None

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        html.Hr(),
        # Use the DataTable prototype component:
        # github.com/plotly/dash-table-experiments
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        )
    ]), df

def register_callbacks_pg1(app):
    @app.callback(
            Output('output-data-upload', 'children'),
            Output('data-store', 'data', allow_duplicate = True),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            prevent_initial_call=True
    )
    def update_data_store_from_uploaded_file(contents, filename):
        print(f"start update data-store from uploaded file")
        if contents is not None:
            children, df = parse_contents(contents, filename)
            #children = [children]
            return children, df.to_json(date_format='iso', orient='split')
        else:
            return None, None
    
    @app.callback(
            Output('data-store', 'data', allow_duplicate=True),
            Input('beer-googles-button', 'n_clicks'),
            prevent_initial_call=True
        )
    def set_dataframe_beer_googles(n_clicks):
        if n_clicks>0:
            print(f"button beer-googles was pressed")
            with open(config.datafile_beer_googles, 'rb') as f:
                result = chardet.detect(f.read())
            df = pd.read_csv(config.datafile_beer_googles, delimiter = '|', encoding=result['encoding'], engine='python')
            print(f"df loaded with ... ")
            print(f"{df.head()}")

            return df.to_json(date_format='iso', orient='split')
        else:
            return None


    @app.callback(
        Output('pg1_datatable', 'data'),
        [Input('data-store', 'data')],
        prevent_initial_call=True
        )
    def update_datatable(jsonified_data):
        try:
            if jsonified_data:
                df = pd.read_json(jsonified_data, orient='split')
                return df.to_dict('records')
            else:
                return None
        except Exception as e:
            print('error:', e)
            return None
