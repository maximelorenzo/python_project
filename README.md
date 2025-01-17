## Enhancements and Features Added to `pybacktestchain`

The **pybacktestchain** package has been significantly enhanced with new functionality to make it more user-friendly, interactive, and versatile. Below is a detailed explanation of the improvements:


### **1. Interactive Dashboard**
A new **Streamlit-powered dashboard** has been developed to allow users to interact with the package more intuitively. This dashboard simplifies the configuration of backtests and makes the package accessible even to users without extensive coding experience.

#### Key Features of the Dashboard:
- **Dynamic Portfolio Selection**: Users can now easily select the stocks they want to include in their portfolio from a predefined list (e.g., S&P 500 companies).
- **Flexible Time Periods**: Users can specify the start and end dates for their backtests with simple date pickers.
- **Initial Cash Allocation**: Users can define the starting amount of cash for their portfolio.
- **Optimization and Risk Model Selection**: The dashboard provides dropdown menus and sliders for selecting optimization methods, risk models, and their parameters, ensuring a smooth and configurable experience.


### **2. Portfolio Optimization Models**
Three new portfolio optimization methods have been added to the package, alongside the original **FirstTwoMoments** model. These methods provide users with a wider range of portfolio construction techniques:

#### **a. FirstTwoMoments (Original)**
- **Objective**: Optimizes the portfolio based on the mean and variance of asset returns.
- **How it Works**:
  - Uses a simplified mean-variance framework to maximize returns for a given level of risk.
  - Suitable for users who want a basic portfolio optimization approach.

#### **b. MaxSharpeRatio (New)**
- **Objective**: Maximizes the portfolio's Sharpe Ratio by balancing returns against risk.
- **Risk-Free Rate**: The user can now specify a dynamic risk-free rate (default: 1% annually), which is factored into the optimization.
- **How it Works**:
  - The optimization focuses on finding a portfolio allocation that maximizes the Sharpe Ratio, a measure of risk-adjusted returns.

#### **c. MinimumVariancePortfolio (New)**
- **Objective**: Constructs a portfolio with the lowest possible variance (i.e., risk).
- **Use Case**: Ideal for risk-averse investors who prioritize stability over returns.
- **How it Works**:
  - The covariance matrix of asset returns is used to identify the portfolio with the minimum variance.
  - Constraints ensure weights sum to 1 and remain non-negative (long-only).

#### **d. EqualRiskContributionPortfolio (New)**
- **Objective**: Allocates capital so that each asset contributes equally to the portfolio's overall risk.
- **Use Case**: Useful for achieving balanced risk exposure across all assets, avoiding concentration in highly volatile stocks.
- **How it Works**:
  - Risk contribution is calculated for each asset based on its volatility and correlation with other assets.
  - Optimization ensures equal contributions while satisfying constraints like weight sums and long-only allocations.


### **3. Risk Models**
In addition to the original risk model, **StopLoss**, a new risk model, **TrailingStop**, has been implemented. Both models allow users to dynamically manage risk during backtests, ensuring that portfolios can respond to adverse market movements.

#### **a. StopLoss (Original)**
- **Objective**: Protects individual positions by automatically selling assets if their price drops below a specified percentage of the entry price.
- **How it Works**:
  - Users can specify a `threshold` (e.g., 10%) representing the maximum acceptable loss.
  - If the asset's current price falls below the threshold (relative to the entry price), the position is liquidated.

#### **b. TrailingStop (New)**
- **Objective**: Dynamically locks in profits by setting a stop-loss price based on the highest price reached since the position was entered.
- **How it Works**:
  - Tracks the **highest price** for each asset since purchase.
  - The stop-loss price is set as `highest_price * (1 - threshold)`.
  - If the current price drops below the stop-loss price, the position is sold.
- **Use Case**: Ideal for trending markets, where users want to secure gains while allowing positions to grow with upward momentum.


### **4. Why These Changes Matter**

The enhancements address several limitations of the original package and open it up to a broader audience:

1. **Ease of Use**: The interactive dashboard makes the package accessible to both technical and non-technical users.
2. **Portfolio Customization**:
   - Users can now choose from multiple optimization methods tailored to their goals, whether it’s maximizing returns, minimizing risk, or balancing risk contributions.
3. **Dynamic Risk Management**:
   - The addition of **TrailingStop** offers a modern and adaptive approach to risk control, complementing the static **StopLoss** model.
4. **Flexibility**:
   - Parameters like the risk-free rate, threshold levels, and optimization methods can now be easily configured, allowing for a highly customizable backtesting process.


### **How to Use the New Features**

#### a. Configuring the Dashboard
1. Launch the dashboard:
   ```bash
   streamlit run path/to/dashboard.py
   ```
2. Use the sidebar to:
   - Select stocks for your portfolio.
   - Set backtesting parameters such as dates and initial cash.
   - Choose an optimization method and its parameters.
   - Select a risk model and configure its threshold.

#### b. Running a Backtest with the CLI
The new features are also accessible via the command-line interface:
```bash
python run_backtest.py '{"initial_date": "2019-01-01", "final_date": "2020-01-01", "universe": ["AAPL", "MSFT"], "optimization_method": "MinimumVariancePortfolio", "risk_model": "StopLoss", "threshold": 0.05}'
```

---

# project

Python Project, M2 203

## Installation

```bash
$ pip install project
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`project` was created by Maxime Lorenzo. It is licensed under the terms of the MIT license.

## Credits

`project` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
