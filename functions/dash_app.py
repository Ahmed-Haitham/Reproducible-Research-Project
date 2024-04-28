import pandas as pd 
import plotly.express as px 

import dash 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output 

# here should be some imports of functions for plots 

app = dash.Dash(__name__)


# Import and clean the data part 
# ------------------------------




# ------------------------------
# App layout 

app.layout = html.Div([
    html.H1("Taxi Fares Prediction Dashboard", style = {'text-align':'center'}), 
    dcc.Graph(id = 'taxi_orders_graph', figure = {})
    ])

# -------------------------------
# App callback 

@app.callback(
    [Output(component_id='taxi_orders_graph', component_property='figure')], 
    [Input(component_id='sth')]
)

def update_graph(option_selected): 
    pass


if __name__ == '__main__': 
    app.run_server(debug = True)