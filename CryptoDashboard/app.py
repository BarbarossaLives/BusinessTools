
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import datetime

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Your CryptoCompare API Key
API_KEY = "5db78f6390952e71ded2bd709e8fd0cf90d794da40ba56060ded8e69b0084ad0" # <-- Replace this with your actual key

# Crypto symbols and names
COINS = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "LTC": "Litecoin",
    "USDT": "Tether",
    "XRP": "XRP",
    "SOL": "Solana"
}

# Buy and Sell thresholds (in USD)
BUY_THRESHOLD = 25000
SELL_THRESHOLD = 35000

# Get current prices
def get_prices():
    symbols = ','.join(COINS.keys())
    url = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={symbols}&tsyms=USD&api_key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Price fetch error: {e}")
        return {}

# Get historical hourly Bitcoin prices (last 24 hours)
def get_coin_history(symbol):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour"
    params = {
        'fsym': symbol,
        'tsym': 'USD',
        'limit': 24,
        'api_key': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['Data']['Data']
    except Exception as e:
        print(f"Historical fetch error for {symbol}: {e}")
        return []


# Layout
app.layout = html.Div([
    html.H1("📊 Crypto Dashboard (CryptoCompare API)"),
    
    html.Div(id='price-container'),

    html.Label("Select Coin for Historical Chart:"),
    dcc.Dropdown(
        id='coin-selector',
        options=[{'label': name, 'value': symbol} for symbol, name in COINS.items()],
        value='BTC',
        clearable=False,
        style={'width': '300px'}
    ),

    html.Div([
        html.Label("Show Buy/Sell Thresholds:"),
        dcc.Checklist(
            id='threshold-toggle',
            options=[
                {'label': 'Buy Threshold', 'value': 'buy'},
                {'label': 'Sell Threshold', 'value': 'sell'}
            ],
            value=['buy', 'sell'],
            inline=True,
            style={'padding': '10px'}
        )
    ]),

    html.Div([
    html.Label("Set Buy/Sell Thresholds (USD):"),

    html.Div([
        html.Label("Buy at:"),
        dcc.Input(
            id='buy-threshold',
            type='number',
            value=25000,
            style={'marginRight': '20px', 'width': '100px'}
        ),

        html.Label("Sell at:"),
        dcc.Input(
            id='sell-threshold',
            type='number',
            value=35000,
            style={'width': '100px'}
        )
    ], style={'padding': '10px'})
]),


    dcc.Graph(id='price-chart'),


    dcc.Interval(id='refresh-interval', interval=60*1000, n_intervals=0)
    ], style={'fontFamily': 'Arial', 'padding': '20px'})


@app.callback(
    Output('price-container', 'children'),
    Output('price-chart', 'figure'),
    Input('refresh-interval', 'n_intervals'),
    Input('coin-selector', 'value'),
    Input('threshold-toggle', 'value'),
    Input('buy-threshold', 'value'),
    Input('sell-threshold', 'value')

)
def update_dashboard(n, selected_coin, toggles, buy_threshold, sell_threshold):

    prices = get_prices()
    history = get_coin_history(selected_coin)


    # Live price cards
    cards = []
    for symbol, name in COINS.items():
        price = prices.get(symbol, {}).get("USD", "N/A")
        cards.append(html.Div(f"{name} ({symbol}): ${price}", style={'padding': '8px', 'fontSize': '18px'}))

    # Extract timestamps and closing prices
    times = [datetime.datetime.fromtimestamp(p['time']).strftime('%H:%M') for p in history]
    values = [p['close'] for p in history]

    chart_data = [{
    'x': times,
    'y': values,
    'type': 'line',
    'name': f'{selected_coin} (24h)',
    'line': {'color': 'blue'}
    }]

    # Conditionally add thresholds
    if 'buy' in toggles and buy_threshold:
        chart_data.append({
            'x': times,
            'y': [buy_threshold] * len(times),
            'type': 'line',
            'name': 'Buy Threshold',
            'line': {'dash': 'dash', 'color': 'green'}
    })

    if 'sell' in toggles and sell_threshold:
        chart_data.append({
            'x': times,
            'y': [sell_threshold] * len(times),
            'type': 'line',
            'name': 'Sell Threshold',
            'line': {'dash': 'dash', 'color': 'red'}
    })


    figure = {
        'data': chart_data,
        'layout': {
            'title': f'{selected_coin} Price - Last 24 Hours',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'USD'},
            'margin': {'l': 40, 'r': 10, 't': 50, 'b': 40}
        }
    }



    return cards, figure


if __name__ == '__main__':
    app.run(debug=True)
