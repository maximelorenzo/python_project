from project.data_stocks import load_sp500_data

# Charger les données
stock_names, stock_tickers = load_sp500_data()

# Afficher les résultats dans le terminal
print("Stock Names:", stock_names)
print("Stock Tickers:", stock_tickers)
