import pandas as pd
import logging
from dataclasses import dataclass
from datetime import datetime

import os 
import pickle
from pybacktestchain.data_module import UNIVERSE_SEC, FirstTwoMoments, get_stocks_data, DataModule, Information
from pybacktestchain.utils import generate_random_name
from pybacktestchain.blockchain import Block, Blockchain
from numba import jit 

from pybacktestchain.broker import Backtest, StopLoss

@dataclass
class CustomBacktest(Backtest):
    def __init__(self, initial_date: datetime, final_date: datetime, universe=None, information_class=None, initial_cash=1000000, **kwargs):
        if not universe or len(universe) == 0:
            raise ValueError("The custom universe cannot be empty. Please provide a valid list of stocks.")

        if information_class is None:
            raise ValueError("An information class (optimization method) must be provided.")

        # Call the base class constructor
        super().__init__(initial_date=initial_date, final_date=final_date, **kwargs)

        # Update attributes with user-defined inputs
        self.universe = universe
        self.information_class = information_class
        self.initial_cash = initial_cash

        # Update the broker's cash dynamically
        self.broker.cash = initial_cash

