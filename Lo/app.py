# # Import Dash library and modules
import dash
# Layout module
import dash_html_components as html
# Charting module and dashboard functionalities
import dash_core_components as dcc
import plotly    
import plotly.express as px
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# example of commit

# Import utilities
import pandas as pd

# Load data
df = pd.read_csv('data/stockdata2.csv', parse_dates=['Date'], usecols=['Date',
																	'stock',
																	'value',
																	'change'])
#df = df.set_index('Date')

#print(df.head())

# Initialise the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the app
app.layout = html.Div()


app.layout = html.Div(children=[
					html.Div(className="row",
							children=[
								html.Div(className="four columns div-user-controls",
									children = [
										html.H2("Dash - Stock Prices in Time"),
										html.P("""Visualising time series with 
													Plotly - Dash"""),
										html.P("""Pick one or more stocks 
												from the dropdown below.""")
											]),
# Defining the left element
								html.Div(className="eight columns div-for-charts bg-grey",
										children=[
											dcc.Graph(id='timeseries',
													config={'displayModeBar':False},
													animate=True,
													figure=px.line(df,
															x='Date',
															y='value',
															color='stock',
															template='plotly_dark'
															).update_layout(
																{'plot_bgcolor':'rgba(0,0,0,0)',
																'paper_bgcolor':'rgba(0,0,0,0)'})
															)
													]
										)
# Defining the right element
								])
					])


#

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

#

html.Div(className='div-for-dropdown',
          children=[
              dcc.Dropdown(id='stockselector',
                           options=get_options(df['stock'].unique()),
                           multi=True,
                           value=[df['stock'].sort_values()[0]],
                           style={'backgroundColor': '#1E1E1E'},
                           className='stockselector')
                    ],
          style={'color': '#1E1E1E'})


#
dcc.Graph(id='timeseries', config={'displayModeBar': False})
dcc.Graph(id='change', config={'displayModeBar': False})


#


@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure


#


# Run the app
if __name__ == '__main__':
	app.run_server(debug=True)