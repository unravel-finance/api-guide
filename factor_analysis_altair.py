# %%

from analysis.utils import get_env

from analysis.alphalens import factor_analysis
from analysis.price import get_price_data
from api.portfolio.factors import get_portfolio_factors_historical
from api.portfolio.tickers import get_tickers

UNRAVEL_API_KEY = get_env("UNRAVEL_API_KEY")
portfolio = "altair"

available_tickers = get_tickers(portfolio, UNRAVEL_API_KEY, universe_size="40")
historical_factors = get_portfolio_factors_historical(
    portfolio, available_tickers, UNRAVEL_API_KEY
)

underlying = get_price_data(available_tickers)


factor_analysis(historical_factors.loc[:, underlying.columns], underlying)

# %%
