
# coding: utf-8

# In[16]:


import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app = dash.Dash(__name__)
server = app.server

df = pd.read_csv(
    'nama_10_gdp_1_Data.csv')


df= df[df.GEO != 'European Union (current composition)']
df= df[df.GEO != 'European Union (without United Kingdom)']
df= df[df.GEO != 'European Union (15 countries)']
df= df[df.GEO != 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)']
df= df[df.GEO != 'Euro area (19 countries)']
df= df[df.GEO != 'Euro area (12 countries)']


available_indicators = df['NA_ITEM'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='TIME--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('TIME--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# ## Exercise 2 practice

# In[ ]:


import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app = dash.Dash(__name__)
server = app.server

df = pd.read_csv(
    'nama_10_gdp_1_Data.csv')


df= df[df.GEO != 'European Union (current composition)']
df= df[df.GEO != 'European Union (without United Kingdom)']
df= df[df.GEO != 'European Union (15 countries)']
df= df[df.GEO != 'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)']
df= df[df.GEO != 'Euro area (19 countries)']
df= df[df.GEO != 'Euro area (12 countries)']




app = dash.Dash()
available_indicators = df['NA_ITEM'].unique()
avaliable_units = df['UNIT'].unique()

country_dropdown = df['GEO'].unique()
country_dropwdown_cleaned = np.delete(country_dropdown,[0,1,2,3,4,5],axis=0)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='countries',
                options=[{'label': i, 'value': i} for i in country_dropwdown_cleaned],
                value='Belgium'
            ),
        
        dcc.Dropdown(
                id='UNITS',
                options=[{'label': i, 'value': i} for i in avaliable_units],
                value='Chain linked volumes, index 2010=100')
        ],
        style={'width': '48%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='yaxis_column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption'
            ),
            dcc.RadioItems(
                id='yaxis_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('countries', 'value'),
     dash.dependencies.Input('yaxis_column', 'value'),
     dash.dependencies.Input('yaxis_type', 'value'),
     dash.dependencies.Input('UNITS', 'value')])


def update_graph(countries, yaxis_column,yaxis_type,
                 UNITS):
    
    dff = df[(df['GEO'] == countries) & (df['UNIT']== UNITS)]
    
    return {
      'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff[dff['NA_ITEM'] == yaxis_column]['Value'],
            mode='lines'
        )],
        
        'layout': go.Layout(
            xaxis={
                'title': 'years'
            },
            yaxis={
                'title': yaxis_column,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 100, 'b': 40, 't': 40, 'r': 100},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

