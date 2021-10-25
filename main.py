import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

for count in range(5):
    limit = 1000
    url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit={}&$offset={}'.format(limit,limit*count) +\
            '&$select=health,steward&$where=health!=\'null\''
    temp = pd.read_json(url)
    if count == 0:
        trees = temp
    trees = trees.append(temp)

num_trees = trees.shape[0]

#fig 1
df_health = trees.groupby('health').count()/num_trees
df_health['health'] = df_health.index
df_health['percent'] = df_health.steward
fig_health = px.bar(df_health, x='health', y='percent')
fig_health.update_layout(xaxis={'categoryorder':'total descending'})

steward_groups = trees.steward.unique()

app.layout = html.Div(children=[
    html.H1(children='NYC Trees'),
    html.Div(children='''
        Health of Trees in NYC
    '''),

    dcc.Graph(
        id='health_nyc_trees',
        figure=fig_health
    ),
    html.Div(children='''
        Health of Trees in NYC by Number of Steward(s)
    '''),
    dcc.Dropdown(
        id='stewards',
        options=[{'label': i, 'value': i} for i in steward_groups]
    ),
    dcc.Graph(
        id='graph_steward'
    )
])

#fig 2
@app.callback(
    Output('graph_steward', 'figure'),
    [Input('stewards', 'value')])


def select_stewards(stewards):
    stewards_trees = trees[trees['steward'] == stewards]
    num_stewards = stewards_trees.shape[0]
    df_stewards = stewards_trees.groupby('health').count()/num_stewards
    df_stewards['health'] = df_stewards.index
    df_stewards['percent'] = df_stewards.steward
    fig_stewards = px.bar(df_stewards, x='health', y='percent')
    fig_stewards.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig_stewards


if __name__ == '__main__':
    app.run_server(debug=True)
