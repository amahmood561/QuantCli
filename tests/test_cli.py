import os
import json
import pytest
from click.testing import CliRunner
from unittest import mock
import pandas as pd
from cli import cli  # Adjust the import based on your file structure

# Helper function to create a sample DataFrame
def create_sample_dataframe():
    data = {
        'Date': pd.date_range(start='2021-01-01', periods=5, freq='D'),
        'Open': [100, 102, 104, 106, 108],
        'High': [101, 103, 105, 107, 109],
        'Low': [99, 101, 103, 105, 107],
        'Close': [100, 102, 104, 106, 108],
        'Volume': [1000, 1500, 2000, 2500, 3000]
    }
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    return df

@pytest.fixture
def runner():
    return CliRunner()

### Test for the `fetch` command ###
@mock.patch('cli.yf.download')
def test_fetch_command(mock_download, runner, tmp_path):
    # Arrange
    symbol = 'AAPL'
    start = '2021-01-01'
    end = '2021-01-05'
    output = tmp_path / 'output.csv'
    
    # Mock the yfinance download to return a sample DataFrame
    mock_download.return_value = create_sample_dataframe()
    
    # Act
    result = runner.invoke(cli, ['fetch', '--symbol', symbol, '--start', start, '--end', end, '--output', str(output)])
    
    # Assert
    assert result.exit_code == 0
    assert f'Data saved to {output}' in result.output
    # Check if the file was created
    assert output.exists()
    # Optionally, verify the contents
    df = pd.read_csv(output, index_col='Date', parse_dates=True)
    assert not df.empty
    assert list(df.columns) == ['Open', 'High', 'Low', 'Close', 'Volume']

### Test for the `indicator` command ###
@mock.patch('cli.pd.read_csv')
def test_indicator_command_SMA(mock_read_csv, runner, tmp_path):
    # Arrange
    indicator_type = 'SMA'
    symbol = 'AAPL'
    period = 2
    input_csv = tmp_path / 'input.csv'
    output_csv = tmp_path / 'output_indicator.csv'
    
    # Create and mock DataFrame
    df = create_sample_dataframe()
    mock_read_csv.return_value = df.copy()
    
    # Act
    result = runner.invoke(cli, [
        'indicator',
        '--type', indicator_type,
        '--symbol', symbol,
        '--period', str(period),
        '--data', str(input_csv),
        '--output', str(output_csv)
    ])
    
    # Assert
    assert result.exit_code == 0
    assert f'Indicator data saved to {output_csv}' in result.output
    # Check if the output file was created
    assert output_csv.exists()
    # Read the output CSV and verify SMA column
    output_df = pd.read_csv(output_csv, index_col='Date', parse_dates=True)
    assert 'SMA' in output_df.columns
    # Verify SMA calculation
    expected_sma = df['Close'].rolling(window=period).mean()
    pd.testing.assert_series_equal(output_df['SMA'], expected_sma.dropna(), check_names=False)

### Test for the `backtest` command ###
@mock.patch('cli.bt.Cerebro')
@mock.patch('cli.pd.read_csv')
def test_backtest_command(mock_read_csv, mock_cerebro, runner, tmp_path):
    # Arrange
    strategy = 'ma_crossover'
    symbol = 'AAPL'
    input_csv = tmp_path / 'input.csv'
    output_dir = tmp_path / 'backtest_results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Mock DataFrame
    df = create_sample_dataframe()
    mock_read_csv.return_value = df.copy()
    
    # Mock Cerebro instance and its methods
    mock_cerebro_instance = mock.Mock()
    mock_cerebro.return_value = mock_cerebro_instance
    mock_strategy = mock.Mock()
    mock_strategy.analyzers.sharpe.get_analysis.return_value = {'sharperatio': 1.5}
    mock_strategy.analyzers.drawdown.get_analysis.return_value = {'max': -10, 'len': 5}
    mock_cerebro_instance.run.return_value = [mock_strategy]
    
    # Act
    result = runner.invoke(cli, [
        'backtest',
        '--strategy', strategy,
        '--symbol', symbol,
        '--data', str(input_csv),
        '--output', str(output_dir)
    ])
    
    # Assert
    assert result.exit_code == 0
    assert f'Backtest results saved to {output_dir}' in result.output
    # Check if JSON result file was created
    result_json = output_dir / f'{symbol}_backtest_results.json'
    assert result_json.exists()
    with open(result_json, 'r') as f:
        data = json.load(f)
    assert data['Sharpe Ratio'] == 1.5
    assert data['Max Drawdown'] == -10
    assert data['Drawdown Period'] == 5
    # Check if plot was attempted to be saved (since plot uses savefig)
    plot_path = output_dir / f'{symbol}_backtest_plot.png'
    mock_cerebro_instance.plot.assert_called_once()

### Test for the `report` command ###
@mock.patch('cli.Environment.get_template')
@mock.patch('cli.HTML')
def test_report_command(mock_html, mock_get_template, runner, tmp_path):
    # Arrange
    portfolio = tmp_path / 'portfolio.json'
    output_pdf = tmp_path / 'report.pdf'
    
    # Sample portfolio data
    portfolio_data = {
        'Sharpe Ratio': 1.5,
        'Max Drawdown': -10,
        'Drawdown Period': 5
    }
    with open(portfolio, 'w') as f:
        json.dump(portfolio_data, f)
    
    # Mock Jinja2 template and rendering
    mock_template = mock.Mock()
    mock_template.render.return_value = '<html>Report</html>'
    mock_get_template.return_value = mock_template
    
    # Mock WeasyPrint HTML
    mock_html_instance = mock.Mock()
    mock_html.return_value = mock_html_instance
    
    # Act
    result = runner.invoke(cli, [
        'report',
        '--portfolio', str(portfolio),
        '--output', str(output_pdf)
    ])
    
    # Assert
    assert result.exit_code == 0
    assert f'Report generated at {output_pdf}' in result.output
    # Check if PDF was attempted to be written
    mock_html_instance.write_pdf.assert_called_once_with(str(output_pdf))

