# %%
import os

import pandas as pd

from factors.alphalens import simplified_factor_analysis
from factors.api import get_portfolio_factors_historical, get_price_series, get_tickers

UNRAVEL_API_KEY = os.environ.get("UNRAVEL_API_KEY")
portfolio = "momentum_enhanced"
available_tickers = get_tickers(portfolio, UNRAVEL_API_KEY)
historical_factors = get_portfolio_factors_historical(
    portfolio, available_tickers, UNRAVEL_API_KEY
)

underlying = pd.DataFrame(
    {
        underlying: get_price_series(underlying, UNRAVEL_API_KEY)
        for underlying in historical_factors.columns
    },
)


simplified_factor_analysis(historical_factors, underlying)

# %%
