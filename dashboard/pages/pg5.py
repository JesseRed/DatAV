import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

# Create app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1(children='Box Plot Example'),

    dcc.Graph(
        id='example-boxplot',
        figure=px.box(df, x="day", y="total_bill", color="smoker")
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)