import dash
from config import colors 
from dash import Input, Output, State, dcc, html, dash_table
import statsmodels.api as sm
from statsmodels.formula.api import ols
import itertools, ast, io
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from markupsafe import Markup
from plotly.subplots import make_subplots
import numpy as np

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
                            #options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                            options=[{'label': html.Span(['select col']), 'value': 'select col'} ],
                            value='select col',
                            style={
                                'width': '200px',
                                'background-color': colors['background-panel'],
                                'color': colors['font1'],
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
                            options=[{'label': html.Span(['select col'], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': 'select col'} ],
                            value='select col',
                            # options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                            # value=df.columns[0],
                            multi=True,
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
                    # options = ['New York City', 'Montréal', 'San Francisco'],
                    # value = ['New York City', 'Montréal'],
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
                                options=[{'label': html.Span(['select col'], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': 'select col'} ],
                                value='select col',
                                # options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                                # value=df.columns[2],
                                style={
                                    'width': '200px',
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
                                options=[{'label': html.Span(['select col'], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': 'select col'} ],
                                value='select col',
                                # options=[{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
                                # value=df.columns[0],
                                multi=True,
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
                    dcc.Graph(id='pg4-boxplot-org_1', style={'display':'none'}),
                    dcc.Graph(id='pg4-boxplot-org_2', style={'display':'none'}),
                    dcc.Graph(id='pg4-boxplot-org_3', style={'display':'none'}),
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
def register_callbacks_pg4(app):
    @app.callback(
        Output('data-store', 'data', allow_duplicate=True),
        Input('filter-button', 'n_clicks'),
        State('textarea-filter','value'),
        State('data-store', 'data'),
        prevent_initial_call=True
    )
    def filter_dataframe(n_clicks, df_filter_string, jsonified_data):
        # print(f"filter_dataframe start...")
        # print(f"filter string = {df_filter_string}")
        if n_clicks>0:
            #print(f"filter_dataframe in nclicks...")
            df = pd.read_json(jsonified_data, orient='split')

            #print(f"{df.head()}")
            try:
                if df_filter_string:
                    df_filtered = df.query(df_filter_string)
                else:
                    df_filtered = df
            except Exception as e:
                print('error:', e)
                df_filtered = df
            return df_filtered.to_json(date_format='iso', orient='split')
        else:
            return jsonified_data

    @app.callback(
        Output('table-output', 'children'),
        Output('pg4-summary-output', 'children'),
        Output('pg4-summary-output-text', 'children'),
        #Output('data-store', 'glm_table'),
        Input('estimate-button', 'n_clicks'),
        State('data-store', 'data'),
        State('column-dropdown', 'value'),
        State('column-dropdown2', 'value'),
        State('checklist_interaction2', 'value'),
        prevent_initial_call=True
    )
    def update_output(n_clicks, jsonified_filtered_data, dependent_variable, independent_variables, interactions2):
        """update the Multivariate Regression output

        Args:
            n_clicks (_type_): _description_
            jsonified_filtered_data (_type_): _description_
            dependent_variable (_type_): _description_
            independent_variables (_type_): _description_
            interactions2 (_type_): _description_

        Returns:
            _type_: _description_
        """
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
        Output('pg4-boxplot-org_1', 'figure'),
        Output('pg4-boxplot-org_1', 'style'),
        Output('pg4-boxplot-org_2', 'figure'),
        Output('pg4-boxplot-org_2', 'style'),
        Output('pg4-boxplot-org_3', 'figure'),
        Output('pg4-boxplot-org_3', 'style'),
        Input('pg4-dropdown-boxplot-org-1', 'value'),
        Input('pg4-dropdown-boxplot-org-2', 'value'),
        State('data-store', 'data'),
        prevent_initial_call=True
    )
    def update_boxplot(selected_column_y, selected_column_x, jsonified_cleaned_data):
        # https://plotly.com/python/reference/
        fig_1 = go.Figure()
        fig_1.update_layout(title='No Data to Display')
        fig_2 = go.Figure()
        fig_2.update_layout(title='No Data to Display')
        fig_3 = go.Figure()
        fig_3.update_layout(title='No Data to Display')
        new_style_1= {'display':'none'}
        new_style_2= {'display':'none'}
        new_style_3= {'display':'none'}
        
        if jsonified_cleaned_data:
            dff = pd.read_json(jsonified_cleaned_data, orient='split')
            #fig = px.box(dff, x='alcohol', y='attractiveness', color='gender', points='all',boxmode='overlay', notched=True)
            if len(selected_column_x) == 1:
                #fig = go.Figure()
                #fig.add_trace(go.Box(x=[1, 2, 3], y=[2, 1, 2]))
                #fig.add_trace(go.Box(x=dff[selected_column_x[0]], y=dff[selected_column_y], 
                #                     marker = {'color': 'green'}))
                fig_1 = px.box(dff, x=selected_column_x, y=selected_column_y)
                new_style_1['display']='block'
                #print(fig)
                #trace_1 = go.box(dff, x=selected_column_x[0], y=selected_column_y)
                #fig.add_trace(trace_1)
            if len(selected_column_x) == 2:
                fig_1 = make_subplots(
                    rows=2, cols=2,
                    specs=[[{}, {}],
                        [{"colspan": 2}, None]],
                    subplot_titles=(selected_column_x[0],selected_column_x[1], 
                                    (f"{selected_column_x[0]} & {selected_column_x[1]}")
                                    )
                                    )
                # fig_tmp = px.box(dff, x=selected_column_x, y=selected_column_y)
                fig_1.add_trace(go.Box(x=dff[selected_column_x[0]], y=dff[selected_column_y]),
                                row=1, col=1)
                fig_1.add_trace(go.Box(x=dff[selected_column_x[1]], y=dff[selected_column_y]),
                                row=1, col=2)
                fig_1.add_trace(go.Box(x=[1, 2, 3], y=[2, 1, 2]),
                                row=2, col=1)
                new_style_1['display'] = 'block'

                fig_2 = px.box(dff, x=selected_column_x, y=selected_column_y, color=selected_column_x[1])
                new_style_2= {'display':'block'}
                
                fig_3 = px.box(dff, x=selected_column_x, y=selected_column_y, color=selected_column_x[0])
                new_style_3= {'display':'block'}
                
                # fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]),
                #                                 row=1, col=1)

                # fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2]),
                #                 row=1, col=2)
                # fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 1, 2]),
                #                 row=2, col=1)

                fig_1.update_layout(showlegend=False, title_text="Specs with Subplot Title")
                

        return fig_1, new_style_1, fig_2, new_style_2, fig_3, new_style_3
                #fig.add_trace(fig2.data[0], row=1, col=2)
            #     figS1 = make_subplots(rows=2, cols=1, subplot_titles=("first", "second"))
            #     # figA = px.box(dff, x=selected_column_x, y=selected_column_y)
            #     # figS1.add_trace(figA.data[0], row=1, col=1)
            #     figS1.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines'), row=1, col=1)
            #     figS2 = make_subplots(rows=1, cols=2, subplot_titles=("first", "second"))
            #     #fig1 = px.box(dff, x=selected_column_x[0], y=selected_column_y)
            #     #fig2 = px.box(dff, x=selected_column_x[1], y=selected_column_y)
            #     figS2.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines'), row=1, col=1)
            #     figS2.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines'), row=1, col=2)
            #     #figS2.add_trace(fig1.data[0], row=1, col=1)
            #     #figS2.add_trace(fig2.data[0], row=1, col=2)
            #     figS1.add_trace(figS2, row=2, col=1)
            #     return figS1
            #fig1 = px.box(dff, x=selected_column_x, y=selected_column_y)
        #     return fig
        #     if len(selected_column_x) == 2:
        #         figS1 = make_subplots(rows=2, cols=1, subplot_titles=("first", "second"))
        #         fig1 = px.box(dff, x=selected_column_x[0], y=selected_column_y)
        #         fig2 = px.box(dff, x=selected_column_x[1], y=selected_column_y)
        #         figS1.add_trace(fig1.data[0], row=1, col=1)
        #         figS1.add_trace(fig2.data[0], row=1, col=1)
        #         figS1.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode='lines'), row=2, col=1)
        #         figS1.update_xaxes(title_text=selected_column_x[0], row=1, col=1)
        #         figS1.update_xaxes(title_text=selected_column_x[1], row=1, col=2)
        #         figS1.update_yaxes(title_text=selected_column_y, row=1, col=1)
        #         figS1.update_layout(height=600, width=800, title_text="Box Plots")
        #         return figS1
        # return fig
        #     if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
        #         figM = make_subplots(rows=1, cols=2, subplot_titles=(selected_column_x[0], selected_column_x[1]))

        #         figM.add_trace(fig1.data[0], row=1, col=1)
        #         figM.add_trace(fig2.data[0], row=1, col=2)
        #         if len(selected_column_x) == 2:
        #             figA = px.box(dff, x=selected_column_x[0], y=selected_column_y)
        #             figB = make_subplots(rows=1, cols=2, subplot_titles=(selected_column_x[0], selected_column_x[1]))
        #             figB.add_trace(figA.data[0], row=1, col=1)
        #             figB.add_trace(figM.data[0], row=1, col=2)
        #             return figB
        #         else:
        #             return figM
        #     else:
        #         figA = px.box(dff, x=selected_column_x, y=selected_column_y)
        #         return figA
        # else:
        #     fig = go.Figure()
        #     fig.update_layout(title='No Data to Display')
        #     return fig

    # @app.callback(
    #     Output('pg4-boxplot-org', 'figure'),
    #     Input('pg4-dropdown-boxplot-org-1', 'value'),
    #     Input('pg4-dropdown-boxplot-org-2', 'value'),
    #     State('data-store', 'data'),
    #     prevent_initial_call=True
    # )
    # def update_boxplot(selected_column_y, selected_column_x, jsonified_cleaned_data):
    #     fig = go.Figure()
    #     fig.update_layout(title='No Data to Display')
    #     if selected_column_x == 'select col' or selected_column_y == 'select col':
    #         return fig
    #     elif jsonified_cleaned_data:
    #         dff = pd.read_json(jsonified_cleaned_data, orient='split')
    #         if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
    #             figM = make_subplots(rows=1, cols=2, subplot_titles=(selected_column_x[0], selected_column_x[1]))
    #             print(f"type(selected_column_x)={type(selected_column_x)}")
    #             print(f"selected_column_x[0]={selected_column_x[1]}")
    #             print(f"type(selected_column_x[0])={type(selected_column_x[1])}")
                
    #             fig1 = px.box(dff, x=selected_column_x[0], y=selected_column_y, color=selected_column_x[1])
    #             fig2 = px.box(dff, x=selected_column_x[1], y=selected_column_y, color=selected_column_x[1])
    #             figM.add_trace(fig1.data[0], row=1, col=1)
    #             figM.add_trace(fig2.data[0], row=1, col=2)
    #             return figM
    #         else:
    #             figA = px.box(dff, x=selected_column_x, y=selected_column_y)
    #             return figA
    #         return fig
    #     else:
    #         fig = go.Figure()
    #         fig.update_layout(title='No Data to Display')
    #         return fig

    #     return fig
    
        # functioning
        # fig = go.Figure()
        # fig.update_layout(title='No Data to Display')
        # if selected_column_x == 'select col' or selected_column_y == 'select col':
        #     return fig
        # elif jsonified_cleaned_data:
        #     dff = pd.read_json(jsonified_cleaned_data, orient='split')
        #     if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
        #         fig = make_subplots(rows=1, cols=2, subplot_titles=(selected_column_x[0], selected_column_x[1]))
        #         fig1 = px.box(dff, x=selected_column_x[0], y=selected_column_y)
        #         print(f"type(figs2)={type(fig1)}")
        #         fig2 = px.box(dff, x=selected_column_x[1], y=selected_column_y, color=selected_column_x[0])
        #         print(f"type(figs2)={type(fig2)}")
        #         fig.add_trace(fig1.data[0], row=1, col=1)
        #         fig.add_trace(fig2.data[0], row=1, col=2)
        #         print(f"type(figx)={type(fig)}")
        #     else:
        #         fig = px.box(dff, x=selected_column_x, y=selected_column_y)
        #         print(f"type(fig)={type(fig)}")
        #     return fig
        # else:
        #     fig = go.Figure()
        #     fig.update_layout(title='No Data to Display')
        #     return fig

        # return fig

        # fig = go.Figure()
        # fig.update_layout(title='No Data to Display')
        # if selected_column_x == 'select col' or selected_column_y == 'select col':
        #     return fig
        # elif jsonified_cleaned_data:
        #     dff = pd.read_json(jsonified_cleaned_data, orient='split')
        #     print(f"dff ....")
        #     print(f"selected_column_y = {selected_column_y}")
        #     print(f"selected_column_x = {selected_column_x}")
        #     print(f"type(selected_column_x) = {type(selected_column_x)}")
        #     #print(dff.head(10))
        #     fig = px.box(dff, x=selected_column_x, y = selected_column_y)
        #     # if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
        #     #     print("is list .... create fig 2")
        #     #     fig2 = px.box(dff, x=selected_column_x[0], y=selected_column_y, color=selected_column_x[1])
        #     #     fig2.update_layout(title='combined')
        #     #     fig.add_trace(fig2.data[0])
        #     return fig
        # else:
        #     fig = go.Figure()
        #     fig.update_layout(title='No Data to Display')
        #     return fig
        print(f"start update_boxplot")
        figs = []
        fig = go.Figure()
        fig.update_layout(title='No Data to Display')
        if selected_column_x == 'select col' or selected_column_y == 'select col':
            return fig
        elif jsonified_cleaned_data:
            dff = pd.read_json(jsonified_cleaned_data, orient='split')
            print(f"dff ....")
            print(dff.head(10))
            print(f"selected_column_y = {selected_column_y}")
            print(f"selected_column_x = {selected_column_x}")
            print(f"type(selected_column_x) = {type(selected_column_x)}")
            print(f"len(figs) = {len(figs)}")
            figs.append(px.box(dff, x=selected_column_x, y=selected_column_y))
            print(f"type(figs1)={type(figs[-1])}")
            print(f"len(figs) = {len(figs)}")
            if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
                figs.append(px.box(dff, x=selected_column_x[0], y=selected_column_y))
                print(f"type(figs2)={type(figs[-1])}")
                figs.append(px.box(dff, x=selected_column_x[1], y=selected_column_y, color=selected_column_x[0]))
                print(f"type(figs3)={type(figs[-1])}")
            print("now we create the subplots")
            fig = make_subplots(rows=2, cols=2, subplot_titles=(selected_column_x[0], "other column"))
            print(f"len(figs) = {len(figs)}")
            for idx, figsub in enumerate(figs):
                print(f"in for loop with idx = {idx}")
                print(f"type(figsub)={type(figsub)}")
                loc_x = (idx+1) % 2
                loc_y = (idx+1) // 2
                print(f"fig.add_traces(figsub[{idx}].data[0], row = {loc_x}, col = {loc_y}")
                fig.add_trace(figsub[idx].data[0], row=loc_x, col=loc_y)
    

        return fig


        #     if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
        #         fig = make_subplots(rows=1, cols=2, subplot_titles=(selected_column_x[0], selected_column_x[1]))
        #         fig1 = px.box(dff, x=selected_column_x[0], y=selected_column_y)
        #         fig2 = px.box(dff, x=selected_column_x[1], y=selected_column_y, color=selected_column_x[0])
        #         fig.add_trace(fig1.data[0], row=1, col=1)
        #         fig.add_trace(fig2.data[0], row=1, col=2)
        #     else:
        #         fig = px.box(dff, x=selected_column_x, y=selected_column_y)
        #     return fig

        # figs = []
        # fig = go.Figure()
        # fig.update_layout(title='No Data to Display')
        # if selected_column_x == 'select col' or selected_column_y == 'select col':
        #     return fig
        # elif jsonified_cleaned_data:
        #     dff = pd.read_json(jsonified_cleaned_data, orient='split')
        #     figs.append(px.box(dff, x=selected_column_x, y=selected_column_y))
        #     if isinstance(selected_column_x, list) and len(selected_column_x) == 2:
        #         figs.append(px.box(dff, x=selected_column_x[0], y=selected_column_y))
        #         figs.append(px.box(dff, x=selected_column_x[1], y=selected_column_y, color=selected_column_x[0]))
        #     fig = make_subplots(rows=2, cols=2, subplot_titles=(selected_column_x[0], "other column"))
        #     for idx, figsub in enumerate(figs):
        #         if isinstance(figsub, go.Box):
        #             loc_x = (idx+1) % 2
        #             loc_y = (idx+1) // 2
        #             fig.add_trace(figsub.data[0], row=loc_x, col=loc_y)
                    
        # return fig
                
        # return fig
        

    @app.callback(
        Output('pg4_datatable', 'data'),
        [Input('data-store', 'data')],
        prevent_initial_call=True
        )
    def update_table(jsonified_cleaned_data):
        try:
            if jsonified_cleaned_data:
                dff = pd.read_json(jsonified_cleaned_data, orient='split')
                return dff.to_dict('records')
            else:
                return None
        except Exception as e:
            print('error:', e)
            return None


    @app.callback(
    Output('checklist_interaction2', 'options'),
    Output('checklist_interaction2', 'value'),
    Input('column-dropdown2', 'value'),
    prevent_initial_call=True
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
    

    
    for dropdown in ['column-dropdown','column-dropdown2','pg4-dropdown-boxplot-org-1','pg4-dropdown-boxplot-org-2']:
        @app.callback(
        Output(dropdown, 'options'),
        Input('data-store', 'data')
        )
        def update_column_dropdown(jsonified_data):
            df = pd.read_json(jsonified_data, orient='split')
            #return [{'label': col,  'value': col} for col in df.columns]
            #return [{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns],
            return [{'label': html.Span([col], style={'color': colors['font1'], 'background-color': colors['background-panel']}), 'value': col} for col in df.columns]
