from datetime import datetime
from project.custom_backtest import CustomBacktest
from project.work import MaxSharpeRatio
from project.work import load_sp500_data
from pybacktestchain.data_module import FirstTwoMoments
from project.work import EqualRiskContributionPortfolio
from project.work import MinimumVariancePortfolio
from pybacktestchain.broker import StopLoss
from project.work import TrailingStop
from project.work import VolatilityStop

custom_backtest = CustomBacktest(
    initial_date=datetime(2019, 1, 1),
    final_date=datetime(2020, 1, 1),
    universe=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'INTC', 'CSCO'],  # Custom universe
    information_class=MinimumVariancePortfolio,  # Custom optimization method
    initial_cash=1000000,  # Custom initial cash
    risk_model=VolatilityStop
)
custom_backtest.run_backtest()



# streamlit run /Users/maxime/Desktop/203/M2/S3/Python/DM/project/src/project/dashboard.py