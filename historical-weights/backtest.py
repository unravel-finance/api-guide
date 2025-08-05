from __future__ import annotations
import pandas as pd
from dataclasses import dataclass

@dataclass
class PortfolioBacktestResult:
    portfolio_returns: pd.Series
    component_returns: pd.DataFrame

    def split(self, start_date, end_date) -> PortfolioBacktestResult:
        return PortfolioBacktestResult(
            portfolio_returns=self.portfolio_returns[start_date:end_date],
            component_returns=self.component_returns[start_date:end_date],
        )


def backtest_portfolio(
    weights: pd.DataFrame,
    underlying: pd.DataFrame,
    transaction_cost: float,
    lag: int,
) -> PortfolioBacktestResult:
    """
    Create a vectorized backtest from a portfolio of weights and the underlying returns.

    Parameters:
        weights: pd.DataFrame
            The weights of the portfolio.
        underlying: pd.DataFrame
            The underlying returns.
        transaction_cost: float
            The transaction cost.
        lag: int
            Additional lag to apply to the signal.
    Returns:
        PortfolioBacktestResult
    """
    assert weights.columns.equals(underlying.columns), "Columns must match"
    underlying = underlying.loc[weights.index]
    weights = weights.ffill().reindex(underlying.index).ffill().copy()
    weights.columns = underlying.columns
    delta_pos = weights.diff(1).abs().fillna(0.0)
    costs = transaction_cost * delta_pos
    returns = (underlying * weights.shift(1 + lag)) - costs
    portfolio_returns = returns.sum(axis="columns")

    return PortfolioBacktestResult(
        portfolio_returns=portfolio_returns,
        component_returns=returns,
    )