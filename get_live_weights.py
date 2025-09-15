# %%
from unravel_client import get_live_weights

from analysis.utils import get_env

UNRAVEL_API_KEY = get_env("UNRAVEL_API_KEY")
portfolio = "beta.5"

live_weights = get_live_weights(portfolio, UNRAVEL_API_KEY)
print(live_weights)
