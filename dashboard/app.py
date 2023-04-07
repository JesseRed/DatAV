import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os


p = os.path.join(os.getcwd(),'..','data_dashboard','CD_20230407')
print(f'p = {p}')
datafile = os.path.join(p,'df_main_spm_results.csv')
print(f'datafile = {datafile}')
# Read the CSV file into a pandas DataFrame
df = pd.read_csv(datafile)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0]
    ),
    html.Div(id='mean-output')
])

# Define the callback function that updates the output
@app.callback(
    Output('mean-output', 'children'),
    [Input('column-dropdown', 'value')]
)
def update_output(column_name):
    selected_column = df[column_name]
    mean_value = selected_column.mean()
    return f"Mean value of '{column_name}': {mean_value:.2f}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)