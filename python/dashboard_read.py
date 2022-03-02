# run with write_to_file.py
import dash
from dash import dcc
from dash import html, callback_context
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import serial

app = dash.Dash(__name__)
#df = pd.read_csv('eeg-car/melissa_push.csv')
df = pd.read_csv('data.csv')
ser = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

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
      ], style={'border':'1px solid', 'border-radius': 10, 'backgroundColor':'#FFFFFF'}),
   html.Div(children=[
      html.H2('Car Controls'),
      html.Div(children=[
         html.Button('Left', id='left', n_clicks=0),
         html.Button('Right', id='right', n_clicks=0),
         html.Button('Forward', id='forward', n_clicks=0),
         html.Button('Backward', id='backward', n_clicks=0),
         html.button('Stop', id='stop', n_clicks=0),
         html.Div(id='car-controls')
      ])
   ])

])


@app.callback(
   Output('live-update-graph', 'figure'),
   [Input('interval-component', 'n_intervals'),Input('dropdown', 'value')]
   #Input('interval-component', 'n_intervals')
)
def update_graph(n, value):
   #print(value)
   current = df.iloc[0:n]
   fig = px.line(current, x='time', y=value).update_traces(mode='lines+markers')
   fig.update_layout({
      'paper_bgcolor': 'rgba(0,0,0,0)'
   })
   #fig.update_xaxes(range=[max(0, current['time'].max() - 0.5), current['time'].max()])
   #fig.update_xaxes(range=[0,0.5])
   fig.update_yaxes(range=[-0.2,1.2])
   return fig

@app.callback(
   Output('car-controls', 'children'),
   Input('left', 'n_clicks'),
   Input('right', 'n_clicks'),
   Input('forward', 'n_clicks'),
   Input('backward', 'n_clicks'),
   Input('stop', 'n_clicks')
)
def update_car_controls(left, right, forward, backward):
   changed_id = [p['prop_id'] for p in callback_context.triggered][0]
   #print(changed_id[:-9])
   ser.write(changed_id[0].encode())

if __name__ == '__main__':
   app.run_server(debug=True)