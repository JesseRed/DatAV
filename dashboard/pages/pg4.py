import dash
from config import df, colors, df_org
from dash import Input, Output, State, dcc, html, dash_table
import statsmodels.api as sm
from statsmodels.formula.api import ols
import itertools, ast, io
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from markupsafe import Markup

dash.register_page(__name__)


layout = html.Div(
    children=[
        # Ueberschrift
        html.Div(
            children=[
                html.H1(
                    children="GLM Analyser",
                    style={
                        'text-align': 'center',
                        'background-color': colors['background-panel'],
                        'color': colors['font1'],
                        'padding': '20px'
                    }
                ),
            ],
            className="mytitle",
        ),
        # main Content of the page
        html.Div(
            children = [
                html.Div(
                    id='dataframe-filter',
                    children = 'Dataframe Filter', 
                    style={
                        'whiteSpace': 'pre-line', 
                        'color': colors['font1'],
                        #'width': '140px',
                        'text-align': 'center',
                        }
                )
            ]
        ),
        html.Div(
            children = [
                html.Div(
                    dcc.Textarea(
                        id='textarea-filter',
                        value="alcohol == '4 Pints' | alcohol == 'None'",
                        style={
                            'height': '50px', 
                            'color': colors['font1'], 
                            'background-color': colors['background-panel'],
                            'border': 'none',
                            'padding': '10px',
                            'box-sizing': 'border-box',
                            'width': '100%',
                        },
                        title= ("Enter a valid Pandas dataframe filter expression \n \
                                multiple statements should be separated by new lines \n \
                                the filter must be in a list, every list statement will \n \
                                be executetd after another"
                        )
                    )
                ),
            ],
            style={
                #'display': 'flex', 
                #'flex-direction': 'row',
                'white-space': 'pre-wrap', 
                'background-color': colors['background-panel'], 
                'color': colors['font1'],
                'border': 'solid 1px',
                'padding': '10px',
                'box-sizing': 'border-box',
                }
        ),
        html.Div(
            children = [
                html.Button('Filter Dataframe', id='filter-button', n_clicks=0, className='standard-button'),
            ],
            style={'padding': '10px'}
        ),
        html.Div(
            children = [
                html.Div(
                    children = [
                        html.Label('Select dependent var'),
                        dcc.Dropdown(
                            id='column-dropdown',
                            options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                            value=df.columns[2],
                            style={
                                'width': '200px',
                                'background-color': colors['background-panel'], 
                                },
                            className='my-dropdown'
                        )
                    ]
                ),
                html.Div(
                    children = [
                        html.Label('Select independent variables'),
                        dcc.Dropdown(
                            id="column-dropdown2",
                            options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                            value=df.columns[0],
                            multi=True,
                            style={
                                'background-color': colors['background-panel'], 
                                },
                            className='my-dropdown'
                        ),
                    ],
                    className="container",
                ),
            ], style={'display': 'flex', 'flex-direction': 'row', 'padding': '10px', 'background-color': colors['background-panel'], 'color':colors['font1']}
        ),
        html.Div(
            children = [
                dcc.Checklist(
                    options = ['New York City', 'Montréal', 'San Francisco'],
                    value = ['New York City', 'Montréal'],
                    labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                    id = 'checklist_interaction2',
                )
            ],
            style={'padding': '10px'}
        ),
        html.Div(
            children = [
                html.Button('Estimate GLM', id='estimate-button', n_clicks=0, className='standard-button'),
            ],
            style={'padding': '10px'}
        ),
        # The output
        html.Div(
            children = [
                html.Div(id="pg4-content", className="pg4-content"),
                html.Div(id='table-output', className='table-output')
            ]
        ),
        html.Div(className='general-spacing'),
        html.Div([
            html.Details([
                html.Summary('More detailed Model Summary ... Click to expand'),
                dcc.Markdown('### Model Summary'),
                html.Div(id = 'pg4-summary-output'),
                html.Div(id = 'pg4-summary-output-text'),
            ]),
        ]),
        html.Div(className='general-spacing'),
        html.Div([
            html.Details([
            html.Summary('General Data Visualisation (independent from GLM) ... Click to expand', style={'background-color':colors['background-color']}),
                    # the Dataframe
            html.Div(
                children = [
                    html.Div(
                        children = [
                            html.Label('Select y'),
                            dcc.Dropdown(
                                id='pg4-dropdown-boxplot-org-1',
                                options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                                value=df.columns[2],
                                style={
                                    'width': '200px',
                                    'background-color': colors['background-panel'], 
                                    },
                                className='my-dropdown'
                            )
                        ]
                    ),
                    html.Div(
                        children = [
                            html.Label('Select x'),
                            dcc.Dropdown(
                                id="pg4-dropdown-boxplot-org-2",
                                options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                                value=df.columns[0],
                                multi=True,
                                style={
                                    'background-color': colors['background-panel'], 
                                    },
                                className='my-dropdown'
                                
                            ),
                        ],
                        className="container",
                    ),
                ], style={'display': 'flex', 'flex-direction': 'row', 'padding': '10px', 'color':colors['font1']}
            ),
            #pg4-dropdown-boxplot-org-1
            html.Div(
                children = [
                    dcc.Graph(id='pg4-boxplot-org')
                ]
            )
            ])
        ]),
        
        html.Div(className='general-spacing'),
        # the Dataframe
        html.Div(
            children = [
            html.Details([
                html.Summary('Filtered Dataframe ... Click to expand', style={'background-color':colors['background-color']}),

                dash_table.DataTable(
                    id = 'pg4_datatable',
                    columns = [{"name": i, "id": i} for i in df.columns],
                    data = df.to_dict('records'),
                    style_table = {
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
def register_callbacks_pg4(app):
    @app.callback(
        Output('data-store', 'data', allow_duplicate=True),
        Input('filter-button', 'n_clicks'),
        State('textarea-filter','value'),
        prevent_initial_call=True
    )
    def filter_dataframe(n_clicks, df_filter_string):
        if n_clicks>0:
            df = df_org.copy()
            try:
                if df_filter_string:
                    df_filtered = df.query(df_filter_string)
                else:
                    df_filtered = df
            except Exception as e:
                print('error:', e)
                df_filtered = df
            df = df_org.copy()
            return df_filtered.to_json(date_format='iso', orient='split')
        else:
            return None

    @app.callback(
        Output('table-output', 'children'),
        Output('pg4-summary-output', 'children'),
        Output('pg4-summary-output-text', 'children'),
        #Output('data-store', 'glm_table'),
        Input('estimate-button', 'n_clicks'),
        State('data-store', 'data'),
        State('column-dropdown', 'value'),
        State('column-dropdown2', 'value'),
        State('checklist_interaction2', 'value')
    )
    def update_output(n_clicks, jsonified_filtered_data, dependent_variable, independent_variables, interactions2):
        if n_clicks>0:
            if jsonified_filtered_data:
                df_filtered = pd.read_json(jsonified_filtered_data, orient='split')
            if isinstance(independent_variables, str):
                independent_variables = independent_variables.split(',')
            formula = dependent_variable + ' ~ ' + ' + '.join(independent_variables)
            if interactions2:
                formula = formula + ' + ' + ' + '.join(interactions2)
            # perform the ANOVA
            model = ols(formula, data=df_filtered).fit()
            table = sm.stats.anova_lm(model, typ=2, float_format='%.4f').reset_index()


            summary = model.summary()
            csv_summary = summary.tables[1].as_csv()
            text_summary = summary.as_text()
            summary_df = pd.read_csv(io.StringIO(csv_summary))
            rows = []

            for i in range(len(table)):
                htmlTR_list = []
                for col in table.columns:
                    if col=='df':
                        htmlTR_list.append(html.Td(f'{table.iloc[i][col]:.0f}'))
                    elif col=='PR(>F)':
                        htmlTR_list.append(html.Td(f'{table.iloc[i][col]:.6f}'))
                    elif col=='sum_sq':
                        htmlTR_list.append(html.Td(f'{table.iloc[i][col]:.1f}'))   
                    elif isinstance(table.iloc[i][col],float):
                        htmlTR_list.append(html.Td(f'{table.iloc[i][col]:.4f}'))
                    else:
                        htmlTR_list.append(html.Td(f'{table.iloc[i][col]}'))
                rows.append(html.Tr(htmlTR_list))
            # convert the table to a HTML table
            table_html = html.Table([
                html.Thead(html.Tr([html.Th(col) for col in table.columns])),
                    html.Tbody(rows)
            ], className='table', style={'color':colors['font1']})

            rows2 = []
            for i in range(len(summary_df)):
                htmlTR_list = []
                for col in summary_df.columns:
                    if 'coef' in col:
                        htmlTR_list.append(html.Td(f'{summary_df.iloc[i][col]:.1f}'))
                    elif 'P>|t|' in col:
                        htmlTR_list.append(html.Td(f'{summary_df.iloc[i][col]:.6f}'))
                    elif ' t ' in col:
                        htmlTR_list.append(html.Td(f'{summary_df.iloc[i][col]:.3f}'))   
                    elif isinstance(summary_df.iloc[i][col],float):
                        htmlTR_list.append(html.Td(f'{summary_df.iloc[i][col]:.2f}'))
                    else:
                        htmlTR_list.append(html.Td(f'{summary_df.iloc[i][col]}'))
                rows2.append(html.Tr(htmlTR_list))
            table_html_summary = html.Table([
                html.Thead(html.Tr([html.Th(col) for col in summary_df.columns])),
                    html.Tbody(rows2)
            ], className='table', style={'color':colors['font1']})
            table_text_summary = dcc.Textarea(value = text_summary,
                                              readOnly = True,
                                              style = {'width':'100%','height': '200px'})
            return table_html, table_html_summary, table_text_summary
        else:
            return None, None, None


    @app.callback(
        Output('pg4-boxplot-org', 'figure'),
        Input('pg4-dropdown-boxplot-org-1', 'value'),
        Input('pg4-dropdown-boxplot-org-2', 'value'),
        Input('data-store', 'data'))
    def update_boxplot(selected_column_y, selected_column_x, jsonified_cleaned_data):
        if jsonified_cleaned_data:
            dff = pd.read_json(jsonified_cleaned_data, orient='split')
            #print(f"dff ....")
            #print(dff.head(10))
            fig = px.box(dff, x=selected_column_x, y = selected_column_y)
            return fig
        else:
            fig = go.Figure()
            fig.update_layout(title='No Data to Display')
            return fig
        # else:
        #     print(f"no jsonfified data")
        #     df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")
        #     fig=px.box(df, x="day", y="total_bill", color="smoker")
        #     return fig
    
    @app.callback(
        Output('pg4_datatable', 'data'),
        [Input('data-store', 'data')])
    def update_table(jsonified_cleaned_data):
        try:
            if jsonified_cleaned_data:
                dff = pd.read_json(jsonified_cleaned_data, orient='split')
                return dff.to_dict('records')
            else:
                return df.to_dict('records')
        except Exception as e:
            print('error:', e)
            return df.to_dict('records')


    @app.callback(
    Output('checklist_interaction2', 'options'),
    Output('checklist_interaction2', 'value'),
    Input('column-dropdown2', 'value')
    )
    def update_checklist_interactions2_options(selected_columns):
        options = []
        value = []

        if isinstance(selected_columns,str):
            pass
        elif isinstance(selected_columns,list):
            # create a list of all possible combinations of two independent variables
            independent_variables = selected_columns
            interactions = list(itertools.combinations(independent_variables, 2))
            options = []
            for interaction in interactions:
                val = interaction[0] + '*' + interaction[1]
                options.append({'label': val, 'value': val})
        else:
            print(f"unknown type in update_checklist_interactions2_options found")

        return options, value