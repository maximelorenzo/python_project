import streamlit as st
import datetime as dt
from pybacktestchain.broker import Backtest, StopLoss
from pybacktestchain.data_module import FirstTwoMoments
import os

# Title of the dashboard
st.title("Backtest Dashboard")

# Sidebar configuration for user inputs
st.sidebar.header("Backtest Parameters")

# Input fields for start and end dates
start_date = dt.datetime.combine(
    st.sidebar.date_input("Start Date", dt.date(2019, 1, 1)), 
    dt.time.min
) # Default start date is January 1, 2019
end_date = dt.datetime.combine(
    st.sidebar.date_input("End Date", dt.date(2020, 1, 1)), 
    dt.time.max
) # Default end date is January 1, 2020

# Input field for initial cash
initial_cash = st.sidebar.number_input(
    "Initial Cash", value=1000000, step=10000
)  # Default initial cash is $1,000,000

# Button to execute the backtest
if st.sidebar.button("Run Backtest"):
    try:
        # Configure the backtest object
        backtest = Backtest(
            initial_date=start_date,  # User-defined start date
            final_date=end_date,  # User-defined end date
            information_class=FirstTwoMoments,  # Uses FirstTwoMoments for portfolio calculations
            risk_model=StopLoss,  # Stop-loss model for risk management
            name_blockchain="dashboard_backtest",  # Save results to a blockchain named "dashboard_backtest"
            verbose=True,  # Enable logging for debugging
        )
        # Set initial cash for the broker
        backtest.broker.cash = initial_cash  # Custom initial cash

        # Run the backtest and display progress
        st.info("Running backtest... Please wait, this may take a while.")
        backtest.run_backtest()  # Execute the backtest logic

        # Generate the option to download the cvs file
        generated_file = f"backtests/{backtest.backtest_name}.csv"

        if os.path.exists(generated_file):
            # Success message upon completion
            st.success("Backtest completed successfully!")
            st.write("Results are ready to download.")

            # Read the CSV file for download
            with open(generated_file, "rb") as file:
                st.download_button(
                    label=f"Download {backtest.backtest_name}.csv",
                    data=file,
                    file_name=f"{backtest.backtest_name}.csv",
                    mime="text/csv",
                )
        else:
            st.error("The backtest completed, but the results file was not found.")

    except Exception as e:
        # Display error messages if the backtest fails
        st.error(f"An error occurred: {e}")

# Instructions for the user
st.write(
    "Configure your backtest in the sidebar, then click on the button Run."
)
