import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import os

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='city-input', type='text', value='Berlin'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container')
])

@app.callback(
    Output('container', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('city-input', 'value')]
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        weather_data = fetch_weather(value, 'your_api_key_here')  # Make sure to replace with your actual API key
        if weather_data:
            return html.Div([
                html.H1(children=f"Weather in {weather_data['name']}"),
                html.P(f"Temperature: {weather_data['main']['temp']}°C"),
                html.P(f"Condition: {weather_data['weather'][0]['description'].capitalize()}"),
                html.P(f"Humidity: {weather_data['main']['humidity']}%"),
                html.P(f"Wind Speed: {weather_data['wind']['speed']} m/s")
            ])
        else:
            return "Failed to retrieve data."
    return "Enter a city and press submit."

def fetch_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': os.environ.get('api_key'), # api_key = 'ebc01ce16f7dc69b0878540694294e9c'
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

if __name__ == '__main__':
    app.run_server(debug=True)
