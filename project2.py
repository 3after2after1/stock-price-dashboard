# In[1]
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import pandas_datareader as pdr
from datetime import datetime as dt
import pandas as pd
# API --> FAMNBCFGN4KTPRV7
app = dash.Dash()
nsdq = pd.read_csv("./NASDAQcompanylist.csv")
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[tic]["Name"] + ' ' + tic
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div([
    html.Div([
        html.H1(children="Stock Ticker Dashboard")
    ]),

    html.Div([
        html.H3("Select stock symbols:", style={'paddingRight': '30px'}),
        dcc.Dropdown(id='stock-symbols',
                     options=options,
                     value=['TSLA', 'AAPL'],
                     multi=True)

    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        html.H3("Select start and end dates:"),
        dcc.DatePickerRange(id='date-picker',
                            min_date_allowed=dt(2018, 1, 1),
                            max_date_allowed=dt.today(),
                            month_format='MMMM Y',
                            start_date=dt(2019, 1, 1),
                            end_date=dt(2019, 11, 30))
    ], style={'width': '30%', 'display': 'inline-block', 'paddingTop': 0, 'verticalAlign': 'top'}),

    html.Div([
        html.Button(id='submit-button', n_clicks=0, children='Submit',
                    style={'fontSize': 24, 'marginLeft': '30px'})
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', }),

    html.Div([
        dcc.Graph(id='line-graph',
                  figure={
                      'data': [
                          {'x': [1, 2], 'y': [3, 1]}
                      ],
                      'layout':{'title': "Stock"}
                  })
    ])
])

# In[1]


@app.callback(Output('line-graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('stock-symbols', 'value'),
               State('date-picker', 'start_date'),
               State('date-picker', 'end_date')])
def update_graph1(n_clicks, value, start_date, end_date):
    start = dt.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for x in value:
        df = pdr.get_data_tiingo(x, start, end, api_key="60d8eaf8353902d2582307d4f9d12ac11ffce7d4")
        df2 = df.reset_index()
        df2['date'] = df2['date'].dt.strftime('%Y-%m-%d')
        df2 = df2.set_index('date')
        traces.append({'x': df2.index, 'y': df2['close'], 'name': x})
    fig = {
        'data': traces,
        'layout': {'title': "Stock"}
    }
    return fig


# In[1]
if __name__ == "__main__":
    app.run_server()
