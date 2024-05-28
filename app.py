import yfinance as yf
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import datetime

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="GokulRaj Dashboard")

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Real-Time Stock Market Dashboard", className='text-center text-primary mb-4'))),
    
    dbc.Row(dbc.Col(dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
            {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
            {'label': 'Reliance (RELIANCE.NS)', 'value': 'RELIANCE.NS'},
            {'label': 'Tata Consultancy Services (TCS.NS)', 'value': 'TCS.NS'},
            {'label': 'Infosys (INFY.NS)', 'value': 'INFY.NS'},
            {'label': 'HDFC Bank (HDFCBANK.NS)', 'value': 'HDFCBANK.NS'},
            {'label': 'ICICI Bank (ICICIBANK.NS)', 'value': 'ICICIBANK.NS'}
        ],
        value='AAPL',
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ))),
    
    dbc.Row([
        dbc.Col(dcc.DatePickerRange(
            id='date-picker-range',
            start_date=(datetime.date.today() - datetime.timedelta(days=30)).isoformat(),
            end_date=datetime.date.today().isoformat(),
            display_format='YYYY-MM-DD',
            style={'margin': 'auto'}
        ), width=6),
    ], className='mb-4'),
    
    dbc.Row([
        dbc.Col(html.Div(id='latest-price', className='text-center'), width=4),
        dbc.Col(html.Div(id='high-price', className='text-center'), width=4),
        dbc.Col(html.Div(id='low-price', className='text-center'), width=4),
    ], className='mb-4'),
    
    dbc.Row(dbc.Col(dcc.Graph(id='stock-graph'), width=12)),
    
    dcc.Interval(
        id='interval-component',
        interval=300000,  # Update every 5 minutes
        n_intervals=0
    )
])

@app.callback(
    [Output('stock-graph', 'figure'),
     Output('latest-price', 'children'),
     Output('high-price', 'children'),
     Output('low-price', 'children')],
    [Input('stock-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(selected_stock, start_date, end_date, n_intervals):
    # Fetch the stock data
    stock_data = yf.Ticker(selected_stock)
    df = stock_data.history(start=start_date, end=end_date, interval='1d')
    
    # Get the latest, highest, and lowest prices
    latest_price = df['Close'].iloc[-1] if not df.empty else None
    high_price = df['High'].max() if not df.empty else None
    low_price = df['Low'].min() if not df.empty else None
    
    # Create the graph
    fig = go.Figure()

    if not df.empty:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='red')
        ))

    fig.update_layout(
        title=f'{selected_stock} Share Price',
        yaxis_title='Stock Price (USD per Share)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False,
        legend_title_text='Legend'
    )
    
    # Prepare the statistics to display
    latest_price_display = f"Latest Price: ${latest_price:.2f}" if latest_price else "No data"
    high_price_display = f"Highest Price: ${high_price:.2f}" if high_price else "No data"
    low_price_display = f"Lowest Price: ${low_price:.2f}" if low_price else "No data"

    return fig, latest_price_display, high_price_display, low_price_display

if __name__ == '__main__':
    app.run_server(debug=True)