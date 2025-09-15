# Unravel API Snippets

Simple Python snippets to get started with the Unravel API for portfolio backtesting and live weight retrieval. These scripts can be converted to Jupyter notebooks using the included conversion script.

## Purpose

This repository provides transparent, easy-to-understand code examples for:

- **Getting Started**: Quick setup and basic usage of the Unravel API
- **Backtest Validation**: Transparent backtesting code to validate portfolio performance
- **Live Weights**: Simple access to current portfolio allocations

## What's Included

### 📊 Portfolio Backtesting

- **`replicate_portfolio_backtest.py`**: Complete backtesting implementation with transaction costs, historical portfolio weights retrieval, and performance visualization

### ⚡ Live Portfolio Data

- **`get_live_weights.py`**: Real-time portfolio weight access for current allocations

### 🔍 Factor Analysis

- **`factor_analysis_altair.py`**: Factor analysis for the Altair portfolio using AlphaLens
- **`factor_analysis_carry_enhanced.py`**: Factor analysis for the Carry Enhanced portfolio
- **`factor_analysis_retail_flow.py`**: Factor analysis for the Retail Flow portfolio
- **`factor_returns_correlation.py`**: Cross-sectional returns correlation analysis between multiple portfolios

### 🛠️ Utilities

- **`convert_to_notebooks.py`**: Script to convert all Python files to Jupyter notebooks
- **`analysis/`**: Utility modules for backtesting, plotting, price data, and factor analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/unravel-finance/api-snippets.git
cd api-snippets

# Install the unravel-client package
pip install unravel-client

# Install other dependencies
pip install -r requirements.txt

# Set up environment variables
export UNRAVEL_API_KEY="your_api_key_here"
```

### Getting Your API Key

1. Visit [Unravel Finance](https://unravel.finance) and sign up for an account
2. Navigate to your API settings to generate an API key
3. Set the environment variable as shown above, or create a `.env` file in the project root:

```bash
echo "UNRAVEL_API_KEY=your_api_key_here" > .env
```

### Dependencies

- `unravel-client`: Official Unravel API client package
- `pandas`: Data manipulation
- `matplotlib`: Visualization
- `requests`: API calls
- `alphalens-reloaded`: Factor analysis
- `finml-utils`: Utilities

## Quick Start

### 1. Convert Python Scripts to Notebooks

The repository includes Python scripts that can be run directly or converted to Jupyter notebooks. To convert them:

```bash
python convert_to_notebooks.py
```

This will create `.ipynb` files for all Python scripts in the root directory. The conversion uses `jupytext` to maintain proper notebook structure.

**Note**: The Python scripts now use the `unravel-client` package instead of the local `api` folder. Make sure to install the package before running the scripts.

### 2. Portfolio Backtesting

Run the complete portfolio backtesting example:

```bash
python replicate_portfolio_backtest.py
# or after conversion:
jupyter notebook replicate_portfolio_backtest.ipynb
```

This script demonstrates:

- Fetching historical portfolio weights
- Getting underlying asset prices
- Running backtests with transaction costs
- Plotting performance results

### 3. Live Portfolio Weights

Get current portfolio allocations:

```bash
python get_live_weights.py
# or after conversion:
jupyter notebook get_live_weights.ipynb
```

### 4. Factor Analysis

Analyze portfolio factors:

```bash
python factor_analysis_altair.py
python factor_analysis_carry_enhanced.py
python factor_analysis_retail_flow.py
# or after conversion:
jupyter notebook factor_analysis_altair.ipynb
jupyter notebook factor_analysis_carry_enhanced.ipynb
jupyter notebook factor_analysis_retail_flow.ipynb
```

### 5. Factor Returns Correlation

Analyze correlations between portfolio returns:

```bash
python factor_returns_correlation.py
# or after conversion:
jupyter notebook factor_returns_correlation.ipynb
```

## Available Portfolios

The scripts demonstrate various Unravel portfolios:

- **`altair`**: Altair portfolio with 40 assets
- **`carry_enhanced`**: Carry Enhanced portfolio with 40 assets
- **`retail_flow`**: Retail Flow portfolio with 30 assets
- **`beta.5`**: Beta portfolio with 5 assets
- **`quarta.40`**: Quarta portfolio with 40 assets
- **`momentum_enhanced.40`**: Momentum Enhanced portfolio with 40 assets
- **`open_interest_divergence.40`**: Open Interest Divergence portfolio with 40 assets
- **`relative_illiquidity.40`**: Relative Illiquidity portfolio with 40 assets

For a complete list of available portfolios and their parameters, visit the [Unravel API Catalog](https://unravel.finance/home/api/catalog/portfolios).

## Migration from Local API

This repository has been updated to use the published `unravel-client` package instead of the local `api` folder. The interface remains the same, but you now need to install the package:

```bash
pip install unravel-client
```

The local `api` folder will be removed in future versions.

## License

These snippets are licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
