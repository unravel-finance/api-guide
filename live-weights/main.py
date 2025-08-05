from api import get_live_weights

UNRAVEL_API_KEY = "DEMO-KEY"  # Demo key last day is restricted to mid 2024
portfolio = "beta"

live_weights = get_live_weights(portfolio, UNRAVEL_API_KEY)
print(live_weights)
