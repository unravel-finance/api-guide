from api import get_portfolio_historical_weights, get_price_series
import pandas as pd
from utils import rebase
from backtest import backtest_portfolio
from plot import plot_backtest_results

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
