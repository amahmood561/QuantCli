import click
import yfinance as yf
import pandas as pd
import backtrader as bt
import matplotlib.pyplot as plt
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# Ensure the 'reports' directory exists
os.makedirs('reports', exist_ok=True)
os.makedirs('backtest_results', exist_ok=True)
os.makedirs('results', exist_ok=True)

@click.group()
def cli():
    """QuantCLI: A CLI tool for Quantitative Finance."""
    pass

@cli.command()
@click.option('--symbol', required=True, help='Stock symbol to fetch data for.')
@click.option('--start', required=True, help='Start date (YYYY-MM-DD).')
@click.option('--end', required=True, help='End date (YYYY-MM-DD).')
@click.option('--output', required=True, type=click.Path(), help='Output CSV file path.')
def fetch(symbol, start, end, output):
    """Fetch historical data for a given symbol."""
    click.echo(f'Fetching data for {symbol} from {start} to {end}...')
    data = yf.download(symbol, start=start, end=end)
    if data.empty:
        click.echo('No data fetched. Please check the symbol and date range.')
        return
    data.to_csv(output)
    click.echo(f'Data saved to {output}')

@cli.command()
@click.option('--type', 'indicator_type', required=True, type=click.Choice(['SMA', 'EMA', 'RSI', 'MACD'], case_sensitive=False), help='Type of indicator to calculate.')
@click.option('--symbol', required=True, help='Stock symbol.')
@click.option('--period', default=14, help='Period for the indicator.')
@click.option('--data', required=True, type=click.Path(exists=True), help='Path to the input CSV data file.')
@click.option('--output', required=True, type=click.Path(), help='Output CSV file path.')
def indicator(indicator_type, symbol, period, data, output):
    """Calculate technical indicators."""
    click.echo(f'Calculating {indicator_type} for {symbol}...')
    df = pd.read_csv(data, index_col='Date', parse_dates=True)
    
    if indicator_type.upper() == 'SMA':
        df['SMA'] = df['Close'].rolling(window=period).mean()
    elif indicator_type.upper() == 'EMA':
        df['EMA'] = df['Close'].ewm(span=period, adjust=False).mean()
    elif indicator_type.upper() == 'RSI':
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
    elif indicator_type.upper() == 'MACD':
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    df.dropna(inplace=True)
    df.to_csv(output)
    click.echo(f'Indicator data saved to {output}')

@cli.command()
@click.option('--strategy', required=True, type=click.Choice(['ma_crossover'], case_sensitive=False), help='Trading strategy to backtest.')
@click.option('--symbol', required=True, help='Stock symbol.')
@click.option('--data', required=True, type=click.Path(exists=True), help='Path to the input CSV data file.')
@click.option('--output', default='backtest_results', type=click.Path(), help='Output directory for backtest results.')
def backtest(strategy, symbol, data, output):
    """Backtest a trading strategy."""
    click.echo(f'Backtesting {strategy} strategy for {symbol}...')
    cerebro = bt.Cerebro()

    # Load data
    df = pd.read_csv(data, index_col='Date', parse_dates=True)
    data_feed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data_feed)

    # Add strategy
    if strategy.lower() == 'ma_crossover':
        from strategies.ma_crossover import MovingAverageCrossover
        cerebro.addstrategy(MovingAverageCrossover)

    # Set initial cash
    cerebro.broker.setcash(100000.0)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    # Run backtest
    results = cerebro.run()
    strat = results[0]

    # Get analyzers
    sharpe = strat.analyzers.sharpe.get_analysis()
    drawdown = strat.analyzers.drawdown.get_analysis()

    # Save results
    result_summary = {
        'Sharpe Ratio': sharpe.get('sharperatio', None),
        'Max Drawdown': drawdown.get('max', None),
        'Drawdown Period': drawdown.get('len', None)
    }

    with open(os.path.join(output, f'{symbol}_backtest_results.json'), 'w') as f:
        json.dump(result_summary, f, indent=4)

    # Plot and save the graph
    cerebro.plot(style='candlestick', savefig=os.path.join(output, f'{symbol}_backtest_plot.png'))
    
    click.echo(f'Backtest results saved to {output}')

@cli.command()
@click.option('--portfolio', required=True, type=click.Path(exists=True), help='Path to the portfolio JSON file.')
@click.option('--output', required=True, type=click.Path(), help='Output report file path (e.g., report.pdf).')
def report(portfolio, output):
    """Generate a performance report."""
    click.echo(f'Generating report from {portfolio}...')
    with open(portfolio, 'r') as f:
        portfolio_data = json.load(f)
    
    # For simplicity, assume portfolio_data contains backtest results
    # You can expand this to include more detailed analysis
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('reports/report_template.html')
    html_out = template.render(portfolio=portfolio_data)

    # Generate PDF
    HTML(string=html_out).write_pdf(output)
    click.echo(f'Report generated at {output}')

if __name__ == '__main__':
    cli()
