import datetime

from finml_utils import get_env

from analysis.backtest import backtest_factor
from analysis.plot import plot_backtest_results
from analysis.price import get_price_series
from api import get_normalized_series

UNRAVEL_API_KEY = get_env("UNRAVEL_API_KEY")
risk_factor = "index_speculative_flow"
ticker = "BTC"
start_date = "2020-01-01"
end_date = datetime.datetime.now().strftime("%Y-%m-%d")
smoothing = 0


risk_factor_signal = get_normalized_series(
    ticker,
    risk_factor,
    UNRAVEL_API_KEY,
    start_date,
    end_date,
    smoothing,
)
price = get_price_series(ticker, start_date, end_date)
price = price[risk_factor_signal.index]
results = backtest_factor(price, risk_factor_signal)

plot_backtest_results(results, ticker, risk_factor, smoothing)
