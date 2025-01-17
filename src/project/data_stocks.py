from pybacktestchain.broker import Backtest
from datetime import datetime
from dataclasses import dataclass
import pandas as pd
import importlib.resources as pkg_resources
import os

@dataclass
class CustomBacktest(Backtest):
    def __init__(self, initial_date: datetime, final_date: datetime, universe=None, **kwargs):
        if not universe or len(universe) == 0:
            raise ValueError("The custom universe cannot be empty. Please provide a valid list of stocks.")
        
        super().__init__(initial_date, final_date, **kwargs)
        self.universe = universe


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