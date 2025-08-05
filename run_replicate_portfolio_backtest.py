import os

import pandas as pd

from analysis.backtest import backtest_portfolio
from analysis.plot import plot_backtest_results
from analysis.price import get_price_series
from analysis.utils import rebase
from api import get_portfolio_historical_weights

UNRAVEL_API_KEY = os.environ.get("UNRAVEL_API_KEY")
portfolio = "beta.5"
start_date = "2022-01-01"
end_date = "2024-06-01"
benchmark_ticker = "BTC"


portfolio_historical_weights = get_portfolio_historical_weights(
    portfolio,
    UNRAVEL_API_KEY,
    start_date,
    end_date,
    smoothing=None,  # This will use the default smoothing please see catalog for default values for each portfolio
)
underlying = pd.DataFrame(
    {
        underlying: get_price_series(underlying, start_date, end_date)
        for underlying in portfolio_historical_weights.columns
    },
)

if benchmark_ticker in underlying.columns:
    benchmark = underlying[benchmark_ticker]
else:
    benchmark = get_price_series(
        benchmark_ticker,
        start_date,
        end_date,
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
