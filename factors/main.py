import os

import pandas as pd

from .alphalens import simplified_factor_analysis
from .api import get_portfolio_factors_historical, get_price_series

UNRAVEL_API_KEY = os.environ.get("UNRAVEL_API_KEY")
portfolio = "momentum_enhanced"
historical_factors = get_portfolio_factors_historical(portfolio, UNRAVEL_API_KEY)
underlying = pd.DataFrame(
    {
        underlying: get_price_series(underlying, UNRAVEL_API_KEY)
        for underlying in historical_factors.columns
    },
)


simplified_factor_analysis(historical_factors, underlying)
