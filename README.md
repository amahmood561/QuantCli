# QuantCLI

**QuantCLI** is a Command-Line Interface (CLI) tool designed for quantitative finance professionals and enthusiasts. It enables users to perform data retrieval, technical analysis, backtesting of trading strategies, and generate comprehensive performance reports directly from the terminal. Streamline your financial modeling and strategy development workflows.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [1. Fetch Historical Data](#1-fetch-historical-data)
  - [2. Calculate Technical Indicators](#2-calculate-technical-indicators)
  - [3. Backtest a Trading Strategy](#3-backtest-a-trading-strategy)
  - [4. Generate a Performance Report](#4-generate-a-performance-report)
- [Available Commands](#available-commands)
- [Example Workflow](#example-workflow)
- [Extending QuantCLI](#extending-quantcli)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

1. **Data Retrieval**
   - Fetch historical and real-time financial data from sources like Yahoo Finance.
   - Supports multiple asset classes: stocks, ETFs, forex, cryptocurrencies, etc.

2. **Technical Indicators**
   - Calculate common technical indicators such as Moving Averages (SMA, EMA), RSI, MACD, and more.
   - Supports custom indicator calculations for advanced users.

3. **Backtesting**
   - Implement and backtest trading strategies using historical data.
   - Provides performance metrics like Sharpe Ratio, Maximum Drawdown, and Win Rate.

4. **Portfolio Analysis**
   - Analyze portfolio performance, diversification, and risk metrics.
   - Offers optimization tools for asset allocation.

5. **Visualization**
   - Generate charts and plots directly in the terminal or save them as image files.
   - Create interactive plots using libraries like Plotly for enhanced analysis.

6. **Automation & Scheduling**
   - Schedule regular data updates and strategy evaluations.
   - Integrates with cron jobs or other scheduling tools.

7. **Reporting**
   - Generate comprehensive reports in formats like PDF or HTML.
   - Receive email notifications for strategy performance or alerts.

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7+**
- **pip** (Python package installer)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/amahmood561/quantcli.git
   cd quantcli
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Libraries**

   ```bash
   pip install -r requirements.txt
   ```

   *If a `requirements.txt` file is not provided, install the necessary libraries manually:*

   ```bash
   pip install click yfinance pandas matplotlib plotly backtrader jinja2 weasyprint
   ```

4. **Make the Script Executable (Optional)**

   If you're on a Unix-like system, you can make the script executable:

   ```bash
   chmod +x quantcli.py
   ```

## Project Structure

```
quantcli/
├── quantcli.py
├── strategies/
│   └── ma_crossover.py
├── reports/
│   └── report_template.html
├── data/
│   └── (your data files)
├── results/
│   └── (indicator results)
├── backtest_results/
│   └── (backtest results and plots)
├── README.md
└── requirements.txt
```

- **quantcli.py**: Main CLI script containing all commands.
- **strategies/**: Directory to store trading strategy scripts.
- **reports/**: Contains HTML templates for generating reports.
- **data/**: Directory to store fetched financial data.
- **results/**: Stores results from technical indicator calculations.
- **backtest_results/**: Contains backtest results and related plots.
- **requirements.txt**: Lists all Python dependencies.
- **README.md**: This README file.

## Usage

After installation, you can use **QuantCLI** through the terminal. Below are the primary commands and their usage.

### 1. Fetch Historical Data

Retrieve historical financial data for a specified symbol within a date range.

**Command:**

```bash
python quantcli.py fetch --symbol SYMBOL --start YYYY-MM-DD --end YYYY-MM-DD --output PATH_TO_CSV
```

**Example:**

Fetch historical data for Apple Inc. (AAPL) from January 1, 2020, to January 1, 2023.

```bash
python quantcli.py fetch --symbol AAPL --start 2020-01-01 --end 2023-01-01 --output data/aapl.csv
```

### 2. Calculate Technical Indicators

Compute technical indicators such as SMA, EMA, RSI, or MACD based on the fetched data.

**Command:**

```bash
python quantcli.py indicator --type INDICATOR_TYPE --symbol SYMBOL --period PERIOD --data PATH_TO_CSV --output PATH_TO_OUTPUT_CSV
```

**Parameters:**

- `--type`: Type of technical indicator (`SMA`, `EMA`, `RSI`, `MACD`).
- `--symbol`: Stock symbol.
- `--period`: Period for the indicator calculation (default is 14).
- `--data`: Path to the input CSV data file.
- `--output`: Path to save the output CSV file with the indicator.

**Example:**

Calculate the Relative Strength Index (RSI) for AAPL with a 14-day period.

```bash
python quantcli.py indicator --type RSI --symbol AAPL --period 14 --data data/aapl.csv --output results/aapl_rsi.csv
```

### 3. Backtest a Trading Strategy

Backtest a specified trading strategy using historical data.

**Command:**

```bash
python quantcli.py backtest --strategy STRATEGY_NAME --symbol SYMBOL --data PATH_TO_CSV --output OUTPUT_DIRECTORY
```

**Parameters:**

- `--strategy`: Name of the trading strategy (`ma_crossover` currently supported).
- `--symbol`: Stock symbol.
- `--data`: Path to the input CSV data file.
- `--output`: Directory to save backtest results and plots (default is `backtest_results`).

**Example:**

Backtest the Moving Average Crossover strategy for AAPL.

```bash
python quantcli.py backtest --strategy ma_crossover --symbol AAPL --data data/aapl.csv --output backtest_results/
```

### 4. Generate a Performance Report

Create a comprehensive performance report from backtest results.

**Command:**

```bash
python quantcli.py report --portfolio PATH_TO_PORTFOLIO_JSON --output PATH_TO_REPORT_PDF
```

**Parameters:**

- `--portfolio`: Path to the portfolio JSON file containing backtest results.
- `--output`: Path to save the generated report (e.g., `reports/AAPL_report.pdf`).

**Example:**

Generate a PDF report for AAPL backtest results.

```bash
python quantcli.py report --portfolio backtest_results/AAPL_backtest_results.json --output reports/AAPL_report.pdf
```

## Available Commands

- **fetch**: Retrieve historical financial data.
- **indicator**: Calculate technical indicators based on fetched data.
- **backtest**: Backtest trading strategies using historical data.
- **report**: Generate performance reports from backtest results.

## Example Workflow

Here's a step-by-step example of how you might use **QuantCLI**:

1. **Fetch Data**

   ```bash
   python quantcli.py fetch --symbol AAPL --start 2020-01-01 --end 2023-01-01 --output data/aapl.csv
   ```

2. **Calculate Indicators**

   Calculate the 14-day RSI:

   ```bash
   python quantcli.py indicator --type RSI --symbol AAPL --period 14 --data data/aapl.csv --output results/aapl_rsi.csv
   ```

3. **Backtest Strategy**

   Backtest the Moving Average Crossover strategy:

   ```bash
   python quantcli.py backtest --strategy ma_crossover --symbol AAPL --data data/aapl.csv --output backtest_results/
   ```

4. **Generate Report**

   Create a PDF report of the backtest results:

   ```bash
   python quantcli.py report --portfolio backtest_results/AAPL_backtest_results.json --output reports/AAPL_report.pdf
   ```

## Extending QuantCLI

**QuantCLI** is designed to be modular and extensible. Here are some ways you can enhance its functionality:

- **Add More Strategies**: Implement additional trading strategies by adding new scripts in the `strategies/` directory and updating the `backtest` command.

- **Support Additional Indicators**: Expand the `indicator` command to include more technical indicators.

- **Portfolio Management**: Introduce commands to manage and analyze a portfolio comprising multiple assets.

- **Real-Time Data Integration**: Incorporate real-time data fetching and live trading capabilities.

- **Machine Learning Models**: Integrate machine learning models for predictive analytics and advanced strategy development.

## Contributing

Contributions are welcome! If you'd like to contribute to **QuantCLI**, please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

Please ensure that your code adheres to the existing style and includes appropriate documentation and tests.



## Contact

For any questions, suggestions, or feedback, please reach out to [amahmood561@gmail.com](mailto:amahmood561@gmail.com).

---

**Enjoy using QuantCLI!** 🚀

Feel free to customize and expand upon this foundation to best fit your specific quantitative finance needs.