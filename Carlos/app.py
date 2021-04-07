# Import Dash library and modules
import dash
# Layout module
import dash_html_components as html
# Charting module and dashboard functionalities
import dash_core_components as dcc
import plotly.express as px


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
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div()



app.layout = html.Div(children=[
					html.Div(className="row",
							children=[
								html.Div(className="four columns div-user-controls",
									children = [
										html.H2("Dash - Stock Prices"),
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





# Run the app
if __name__ == '__main__':
	app.run_server(debug=True)