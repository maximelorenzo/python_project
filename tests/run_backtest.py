import sys
import json
from project.custom_backtest import CustomBacktest
import datetime as dt

def main():
    # Read arguments from JSON passed by the dashboard
    args = json.loads(sys.argv[1])
    
    # Parse input arguments
    initial_date = dt.datetime.strptime(args['initial_date'], '%Y-%m-%d')
    final_date = dt.datetime.strptime(args['final_date'], '%Y-%m-%d')
    universe = args['universe']
    initial_cash = args['initial_cash']
    optimization_method = args['optimization_method']
    risk_free_rate = args.get('risk_free_rate', 0.01)
    
    # Import the selected optimization method
    if optimization_method == "FirstTwoMoments":
        from pybacktestchain.data_module import FirstTwoMoments as SelectedClass
    elif optimization_method == "MaxSharpeRatio":
        from project.work import MaxSharpeRatio as SelectedClass
    elif optimization_method == "EqualRiskContributionPortfolio":
        from project.work import EqualRiskContributionPortfolio as SelectedClass
    elif optimization_method == "MinimumVariancePortfolio":
        from project.work import MinimumVariancePortfolio as SelectedClass
    else:
        raise ValueError(f"Unknown optimization method: {optimization_method}")

    # Run the backtest
    custom_backtest = CustomBacktest(
        initial_date=initial_date,
        final_date=final_date,
        universe=universe,
        information_class=SelectedClass,
        initial_cash=initial_cash,
        risk_free_rate=risk_free_rate
    )
    
    custom_backtest.run_backtest()

    # Output success message
    print(f"Backtest completed successfully! Output file: backtests/{custom_backtest.backtest_name}.csv")

if __name__ == "__main__":
    main()
