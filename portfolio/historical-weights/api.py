import pandas as pd
import requests

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
    ticker: str,
    API_KEY: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    """
    Fetch the price series from the Unravel API.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., 'BTC')
        API_KEY (str): The API key to use for the request
        start_date (str | None): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format

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
