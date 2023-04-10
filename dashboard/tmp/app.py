import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(
    children = [
    dcc.Input(id='input-1', type='text', value=''),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-div'),
    dcc.Store(id='data-store')
    ]
    )

@app.callback(Output('data-store', 'data'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1', 'value')])
def save_data(n_clicks, input_value):
    return input_value

@app.callback(Output('output-div', 'children'),
              [Input('data-store', 'data')])
def display_data(data):
    return f"The saved data is: {data}"

if __name__ == '__main__':
    app.run_server(debug=True)
