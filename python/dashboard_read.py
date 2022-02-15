# run with write_to_file.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
df = pd.read_csv('data.csv')

app.layout = html.Div(children=[
   html.H1('EEG DATA'),
   dcc.Dropdown(id='dropdown', options=[{'label': name, 'value': name} for name in df.columns[1:]], value='/fac/uAct/frown', multi=True),
   html.Br(),
   html.Div(children=[
      dcc.Graph(id='live-update-graph'),
         dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
         )
      ], style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'})
])


@app.callback(
   Output('live-update-graph', 'figure'),
   [Input('interval-component', 'n_intervals'),Input('dropdown', 'value')]
   #Input('interval-component', 'n_intervals')
)
def update_graph(n, value):
   current = pd.read_csv('data.csv')
   print(current)
   fig = px.line(current, x='time', y=value).update_traces(mode='lines+markers')
   fig.update_layout({
      'paper_bgcolor': 'rgba(0,0,0,0)'
   })
   fig.update_xaxes(range=[max(0, current['time'].max() - 0.5), current['time'].max()])
   return fig

if __name__ == '__main__':
   app.run_server(debug=True)