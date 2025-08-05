# %%
from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import requests

# plotting.py


def plot_backtest_results(
    cumulative_returns: pd.Series,
    benchmark: pd.Series,
    portfolio: str,
    figsize=(12, 10),
):
    """
    Plot backtest results with performance chart and signal.

    Args:
        results (pd.DataFrame): DataFrame containing backtest results with
                               'cumulative_returns', 'price_rebased', and 'signal' columns
        figsize (tuple): Figure size as (width, height) in inches
    """
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=figsize, gridspec_kw={"height_ratios": [2, 1]}
    )

    ax1.plot(
        cumulative_returns.index,
        cumulative_returns,
        label="Strategy Returns",
        color="darkBlue",
    )
    ax1.plot(
        benchmark.index,
        benchmark,
        label=f"Benchmark ({benchmark.name})",
        color="gray",
    )
    ax1.set_title("Performance of Portfolio", fontsize=14)
    ax1.legend()
    ax1.grid(True, axis="y", linestyle="--")

    ax2.plot(
        cumulative_returns.index,
        to_drawdown(cumulative_returns),
        label="Drawdown Portfolio",
        color="red",
    )
    ax2.plot(
        benchmark.index,
        to_drawdown(benchmark),
        label="Drawdown Benchmark",
        color="gray",
    )
    ax2.set_title(f"Portfolio {portfolio}")
    ax2.legend()
    ax2.grid(True, axis="y", linestyle="--")

    plt.tight_layout()
    plt.show()

    return fig, (ax1, ax2)


# --------------------------------------------------

# backtest.py


@dataclass
class PortfolioBacktestResult:
    portfolio_returns: pd.Series
    component_returns: pd.DataFrame

    def split(self, start_date, end_date) -> PortfolioBacktestResult:
        return PortfolioBacktestResult(
            portfolio_returns=self.portfolio_returns[start_date:end_date],
            component_returns=self.component_returns[start_date:end_date],
        )


def backtest_portfolio(
    weights: pd.DataFrame,
    underlying: pd.DataFrame,
    transaction_cost: float,
    lag: int,
) -> PortfolioBacktestResult:
    """
    Create a vectorized backtest from a portfolio of weights and the underlying returns.

    Parameters:
        weights: pd.DataFrame
            The weights of the portfolio.
        underlying: pd.DataFrame
            The underlying returns.
        transaction_cost: float
            The transaction cost.
        lag: int
            Additional lag to apply to the signal.
    Returns:
        PortfolioBacktestResult
    """
    assert weights.columns.equals(underlying.columns), "Columns must match"
    underlying = underlying.loc[weights.index]
    weights = weights.ffill().reindex(underlying.index).ffill().copy()
    weights.columns = underlying.columns
    delta_pos = weights.diff(1).abs().fillna(0.0)
    costs = transaction_cost * delta_pos
    returns = (underlying * weights.shift(1 + lag)) - costs
    portfolio_returns = returns.sum(axis="columns")

    return PortfolioBacktestResult(
        portfolio_returns=portfolio_returns,
        component_returns=returns,
    )


# --------------------------------------------------

# api.py


BASEAPI = "https://unravel.finance/api/v1"


def get_portfolio_historical_weights(
    portfolio: str,
    start_date: str,
    end_date: str,
    API_KEY: str,
) -> pd.DataFrame:
    """
    Fetch normalized risk signal data from the Unravel API.

    Args:
        portfolio (str): The portfolio ID
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        API_KEY (str): The API key to use for the request
    Returns:
        pd.Series: Time series of the risk signal with datetime index
    """
    url = f"{BASEAPI}/portfolio/historical-weights"
    params = {
        "portfolio": portfolio,
        "start_date": start_date,
        "end_date": end_date,
    }
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    assert (
        response.status_code == 200
    ), f"Error fetching portfolio for {portfolio}, response: {response.json()}"

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    )


def get_price_series(
    ticker: str, start_date: str, end_date: str, API_KEY: str
) -> pd.Series:
    """
    Fetch the price series from the Unravel API.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., 'BTC')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        API_KEY (str): The API key to use for the request

    Returns:
        pd.Series: Time series of the risk signal with datetime index
    """
    url = f"{BASEAPI}/price"
    params = {"ticker": ticker, "start_date": start_date, "end_date": end_date}
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    assert (
        response.status_code == 200
    ), f"Error fetching price series for {ticker}, response: {response.json()}"

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        ticker
    )


def rebase(prices: pd.Series) -> pd.Series:
    """Rebase a price series to 1.0"""
    return prices / prices.iloc[0]


def to_drawdown(prices: pd.Series) -> pd.Series:
    """
    Calculate drawdowns from a price series.

    Args:
        prices (pd.Series): Time series of prices

    Returns:
        pd.Series: Drawdowns as percentage decline from previous peak
    """
    # Calculate running maximum
    running_max = prices.cummax()

    # Calculate drawdown as (current_price - running_max) / running_max
    drawdowns = (prices - running_max) / running_max

    return drawdowns


# --------------------------------------------------

# main.py


UNRAVEL_API_KEY = "DEMO-KEY"
portfolio = "beta"
start_date = "2022-01-01"
end_date = "2024-06-01"
benchmark_ticker = "BTC"


portfolio_historical_weights = get_portfolio_historical_weights(
    portfolio, start_date, end_date, UNRAVEL_API_KEY
)
underlying = pd.DataFrame(
    {
        underlying: get_price_series(underlying, start_date, end_date, UNRAVEL_API_KEY)
        for underlying in portfolio_historical_weights.columns
    },
)

if benchmark_ticker in underlying.columns:
    benchmark = underlying[benchmark_ticker]
else:
    benchmark = get_price_series(
        benchmark_ticker, start_date, end_date, UNRAVEL_API_KEY
    )

underlying_returns = underlying.pct_change()
results = backtest_portfolio(
    weights=portfolio_historical_weights,
    underlying=underlying_returns,
    transaction_cost=0.001,
    lag=0,
)
portfolio_cumulative_returns = (1 + results.portfolio_returns).cumprod()
plot_backtest_results(
    rebase(portfolio_cumulative_returns), rebase(benchmark), portfolio
)
