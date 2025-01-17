import streamlit as st
import subprocess
import json
import datetime as dt
import os
from project.work import load_sp500_data

stock_names, stock_tickers = load_sp500_data()

# Title of the dashboard
st.title("Backtest Dashboard")

# Sidebar configuration for user inputs
st.sidebar.header("Backtest Parameters")

# Input fields for start and end dates
start_date = st.sidebar.date_input("Start Date", dt.date(2019, 1, 1))
end_date = st.sidebar.date_input("End Date", dt.date(2020, 1, 1))

# Validate date range
if start_date >= end_date:
    st.sidebar.error("End Date must be after Start Date.")

# Input field for initial cash
initial_cash = st.sidebar.number_input("Initial Cash", value=1000000, step=10000)

# Input field for selecting tickers
selected_stock_names = st.sidebar.multiselect(
    "Select Tickers", 
    options=stock_names,
    default=['Apple Inc.', 'Microsoft', 'Alphabet Inc. (Class A)', 'Amazon', 'Meta Platforms', 'Tesla, Inc.', 'Nvidia', 'Intel', 'Cisco', 'Netflix']  # Default selected tickers
)
selected_tickers = [stock_tickers[name] for name in selected_stock_names if name in stock_tickers]

# Dropdown to choose the optimization method
optimization_methods = ["FirstTwoMoments", "MaxSharpeRatio"]
selected_method_name = st.sidebar.selectbox("Select Optimization Method", options=optimization_methods)

risk_free_rate = 0.01  # Taux par défaut
if selected_method_name == "MaxSharpeRatio":
    risk_free_rate = st.sidebar.number_input(
        "Risk-Free Rate (Annual)", 
        min_value=0.0, 
        max_value=0.1, 
        value=0.01, 
        step=0.001,
        format="%.4f"
    )

# Button to execute the backtest
if st.sidebar.button("Run Backtest"):
    if not selected_tickers:
        st.error("Please select at least one ticker.")
    else:
        try:
            # Prepare arguments for the script
            args = {
                "initial_date": start_date.strftime('%Y-%m-%d'),
                "final_date": end_date.strftime('%Y-%m-%d'),
                "universe": selected_tickers,
                "initial_cash": initial_cash,
                "optimization_method": selected_method_name,
                "risk_free_rate": risk_free_rate
            }

            # Call the script
            with st.spinner("Running backtest... Please wait."):
                result = subprocess.run(
                    ['python', os.path.join(os.path.dirname(__file__), "../../tests/run_backtest.py"), json.dumps(args)],
                    text=True,
                    capture_output=True
                )

            # Handle the script output
            if result.returncode == 0:
                # Display parameters
                st.success("Backtest completed successfully!")
                st.write("### Backtest Summary")
                st.write(f"- **Start Date:** {start_date}")
                st.write(f"- **End Date:** {end_date}")
                st.write(f"- **Selected Stocks:** {selected_stock_names}")
                st.write(f"- **Optimization Method:** {selected_method_name}")
                st.write(f"- **Initial Cash:** ${initial_cash:,.2f}")


                # Extract the file path from the output
                backtest_name = result.stdout.strip().split(": ")[-1]
                generated_file = backtest_name
                # Check if the file exists
                if os.path.exists(generated_file):
                    # Read the CSV file for download
                    with open(generated_file, "rb") as file:
                        st.download_button(
                            label="Download results.csv",
                            data=file,
                            file_name="results.csv",
                            mime="text/csv",
                        )

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Instructions for the user
st.write(
    "Configure your backtest in the sidebar, then click on the 'Run Backtest' button."
)