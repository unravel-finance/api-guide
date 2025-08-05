import pandas as pd

from .alphalens import simplified_factor_analysis
from .api import get_portfolio_factors_historical, get_price_series

UNRAVEL_API_KEY = "785cc813-a52e-4c30-829c-d5f30759c729"
portfolio = "momentum_enhanced"
historical_factors = get_portfolio_factors_historical(portfolio, UNRAVEL_API_KEY)
underlying = pd.DataFrame(
    {
        underlying: get_price_series(underlying, UNRAVEL_API_KEY)
        for underlying in historical_factors.columns
    },
)


simplified_factor_analysis(historical_factors, underlying)
