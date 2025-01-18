from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import numpy as np
from scipy.optimize import minimize
import pandas as pd
from pybacktestchain.data_module import DataModule, FirstTwoMoments
import os
from pybacktestchain.broker import Broker, RiskModel
from project.work2 import Broker
from pybacktestchain.broker import Position


def load_sp500_data():
    """
    Load S&P 500 data from a CSV file included in the package.

    Returns:
        tuple: (list of stock names, dict mapping names to tickers)
    """
    try:
        csv_file_path = os.path.join(os.path.dirname(__file__), "../../docs/SP500.csv")
        sp500_data = pd.read_csv(csv_file_path)
        stock_names = sp500_data.iloc[:, 1].tolist()  # Second column for stock names
        stock_tickers = sp500_data.set_index(sp500_data.columns[1])[sp500_data.columns[0]].to_dict()  # Map Name to Ticker

        return stock_names, stock_tickers
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return [], {}


@dataclass
class MaxSharpeRatio(FirstTwoMoments):
    risk_free_rate: float = 0.01  # Annual risk-free rate (e.g., 1%)

    def compute_portfolio(self, t: datetime, information_set):
        try:
            mu = information_set['expected_return']
            Sigma = information_set['covariance_matrix']
            rf = self.risk_free_rate / 252  # Convert annual risk-free rate to daily
            n = len(mu)

            # Define the negative Sharpe Ratio as the objective function
            def sharpe_ratio_neg(weights):
                portfolio_return = weights.dot(mu)
                portfolio_volatility = np.sqrt(weights.dot(Sigma).dot(weights))
                return -(portfolio_return - rf) / portfolio_volatility

            # Constraints: weights sum to 1
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            # Bounds: Long-only portfolio
            bounds = [(0.0, 1.0)] * n
            # Initial guess: equal weights
            x0 = np.ones(n) / n

            # Minimize the negative Sharpe Ratio
            res = minimize(sharpe_ratio_neg, x0, constraints=cons, bounds=bounds)

            # Prepare portfolio dictionary
            portfolio = {k: None for k in information_set['companies']}
            if res.success:
                for i, company in enumerate(information_set['companies']):
                    portfolio[company] = res.x[i]
            else:
                raise Exception("Optimization did not converge")

            return portfolio
        except Exception as e:
            # If an error occurs, return equal weights and log the issue
            logging.warning("Error computing portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1 / len(information_set['companies']) for k in information_set['companies']}


@dataclass
class MinimumVariancePortfolio(FirstTwoMoments):
    def compute_portfolio(self, t: datetime, information_set):
        try:
            Sigma = information_set['covariance_matrix']
            n = len(Sigma)

            # Define the portfolio variance as the objective function
            def portfolio_variance(weights):
                return weights.dot(Sigma).dot(weights)

            # Constraints: weights must sum to 1
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            # Bounds: Long-only portfolio (weights between 0 and 1)
            bounds = [(0.0, 1.0)] * n
            # Initial guess: equal weights
            x0 = np.ones(n) / n

            # Minimize the portfolio variance
            res = minimize(portfolio_variance, x0, constraints=cons, bounds=bounds)

            # Prepare portfolio dictionary
            portfolio = {k: None for k in information_set['companies']}
            if res.success:
                for i, company in enumerate(information_set['companies']):
                    portfolio[company] = res.x[i]
            else:
                raise Exception("Optimization did not converge")

            return portfolio
        except Exception as e:
            # If an error occurs, return equal weights and log the issue
            logging.warning("Error computing portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1 / len(information_set['companies']) for k in information_set['companies']}

@dataclass
class EqualRiskContributionPortfolio(FirstTwoMoments):
    def compute_portfolio(self, t: datetime, information_set):
        try:
            Sigma = information_set['covariance_matrix']
            n = len(Sigma)

            # Function to compute the risk contributions
            def risk_contributions(weights):
                portfolio_variance = weights.dot(Sigma).dot(weights)
                marginal_risk = Sigma.dot(weights)
                return weights * marginal_risk / portfolio_variance

            # Objective: minimize the squared difference between risk contributions
            def objective(weights):
                rc = risk_contributions(weights)
                avg_rc = np.mean(rc)
                return np.sum((rc - avg_rc) ** 2)

            # Constraints: weights sum to 1
            cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

            # Bounds: Long-only portfolio (weights between 0 and 1)
            bounds = [(0.0, 1.0)] * n

            # Initial guess: equal weights
            x0 = np.ones(n) / n

            # Minimize the objective
            res = minimize(objective, x0, constraints=cons, bounds=bounds)

            # Prepare the portfolio dictionary
            portfolio = {k: None for k in information_set['companies']}
            if res.success:
                for i, company in enumerate(information_set['companies']):
                    portfolio[company] = res.x[i]
            else:
                raise Exception("Optimization did not converge")

            return portfolio
        except Exception as e:
            # If an error occurs, return equal weights and log the issue
            logging.warning("Error computing portfolio, returning equal weight portfolio")
            logging.warning(e)
            return {k: 1 / len(information_set['companies']) for k in information_set['companies']}


@dataclass
class TrailingStop:
    threshold: float = 0.1  # Default trailing stop threshold

    def trigger_stop_loss(self, t, portfolio, prices, broker):
        """
        Triggers a sell if the current price falls below the trailing stop.
        
        Args:
            t (datetime): Current timestamp.
            portfolio (dict): Portfolio weights or positions.
            prices (dict): Current market prices for the universe of stocks.
            broker (Broker): The broker managing the portfolio.
        """
        # Calculate the highest prices on-the-fly
        highest_prices = {
            ticker: max(broker.entry_prices.get(ticker, 0), prices.get(ticker, 0))
            for ticker in broker.positions.keys()
        }

        for ticker, position in list(broker.positions.items()):
            current_price = prices.get(ticker, None)
            if current_price is None:
                logging.warning(f"Price for {ticker} not available at {t}")
                continue
            
            highest_price = highest_prices.get(ticker, 0)
            # Calculate the percentage loss from the highest price
            loss = (current_price - highest_price) / highest_price
            if loss < -self.threshold:
                logging.info(f"Trailing stop triggered for {ticker} at {t}. Selling all shares.")
                broker.sell(ticker, position.quantity, current_price, t)


from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import logging
from datetime import datetime


@dataclass
class VolatilityStop:
    threshold: float  # Volatility threshold (e.g., 0.02 for 2%)
    window: int = 20  # Rolling window size for volatility calculation
    price_history: dict = field(default_factory=lambda: {})  # Stores historical prices

    def update_price_history(self, ticker: str, price: float):
        """Update the price history for a specific ticker."""
        if ticker not in self.price_history:
            self.price_history[ticker] = []
        self.price_history[ticker].append(price)
        # Keep only the last `window` prices
        self.price_history[ticker] = self.price_history[ticker][-self.window :]

    def calculate_volatility(self, ticker: str) -> float:
        """Calculate rolling volatility for a specific ticker."""
        if ticker not in self.price_history or len(self.price_history[ticker]) < self.window:
            return 0.0  # Not enough data to calculate volatility
        # Convert to percentage returns
        prices = pd.Series(self.price_history[ticker])
        returns = prices.pct_change().dropna()
        return returns.std()

    def trigger_stop_loss(self, t: datetime, portfolio: dict, prices: dict, broker):
        """
        Trigger stop-loss actions based on volatility.
        
        Args:
            t (datetime): Current timestamp.
            portfolio (dict): Portfolio weights or positions.
            prices (dict): Current market prices for the universe of stocks.
            broker: The broker managing the portfolio.
        """
        for ticker, position in list(broker.positions.items()):
            current_price = prices.get(ticker, None)
            if current_price is None:
                logging.warning(f"Price for {ticker} not available at {t}")
                continue

            # Update price history and calculate volatility
            self.update_price_history(ticker, current_price)
            volatility = self.calculate_volatility(ticker)

            if volatility > self.threshold:
                logging.info(
                    f"Volatility stop triggered for {ticker} at {t}. "
                    f"Volatility: {volatility:.4f}, Threshold: {self.threshold:.4f}"
                )
                broker.sell(ticker, position.quantity, current_price, t)

