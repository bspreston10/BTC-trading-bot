import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON Data
with open("/Users/bennett/Desktop/trading_bot/portfolio.json", "r") as f:
    portfolio = json.load(f)

# Load Trade History Data
trade_history = pd.read_csv('/Users/bennett/Desktop/trading_bot/simulated_trades_log.csv')

# Add a refresh button
if st.sidebar.button("Refresh Data"):
    st.query_params = {"refresh": "true"}

# Data Cleaning and Preprocessing
# Ensure correct data types
trade_history["Timestamp"] = pd.to_datetime(trade_history["Timestamp"])
trade_history["Entry Price"] = pd.to_numeric(trade_history["Entry Price"], errors="coerce")
trade_history["Trade Amount"] = pd.to_numeric(trade_history["Trade Amount"], errors="coerce")
trade_history.dropna(inplace=True)

# Add Trade Type (Buy/Sell) from Signal
trade_history["Trade Type"] = trade_history["Signal"].str.contains("Buy").map({True: "Buy", False: "Sell"})

# Extract Portfolio Details
cash = portfolio["cash"]
positions = portfolio["positions"]

# Convert Positions to DataFrame
positions_df = pd.DataFrame(positions).T
positions_df["Total Value"] = positions_df["quantity"] * positions_df["entry_price"]

# Streamlit App
st.title("Trading Bot Dashboard")
st.sidebar.header("Filters & Navigation")

# Sidebar Navigation
tabs = st.sidebar.radio("Go to:", ["Portfolio Summary", "Trade History", "Performance Metrics"])

# Portfolio Summary
if tabs == "Portfolio Summary":
    st.header("Portfolio Summary")

    # Display Cash
    st.metric("Cash Available", f"${cash:,.2f}")

    # Display Positions Table
    st.subheader("Open Positions")
    st.dataframe(positions_df)

    # Visualize Total Value per Position
    st.subheader("Portfolio Allocation")
    fig, ax = plt.subplots()
    positions_df["Total Value"].plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Portfolio Value by Asset")
    ax.set_ylabel("Value ($)")
    ax.set_xlabel("Asset")
    st.pyplot(fig)

# Trade History
if tabs == "Trade History":
    st.header("Trade History")

    # Display Entire Trade History
    st.subheader("All Trades")
    st.dataframe(trade_history)

    # Add Filters for Trade History
    st.subheader("Filter Trades by Asset")
    selected_asset = st.selectbox("Select an Asset", trade_history["Symbol"].unique())
    filtered_trades = trade_history[trade_history["Symbol"] == selected_asset]
    st.write(f"Showing trades for: {selected_asset}")
    st.dataframe(filtered_trades)

# Performance Metrics
if tabs == "Performance Metrics":
    st.header("Performance Metrics")

    # Total Portfolio Value
    total_value = cash + positions_df["Total Value"].sum()
    st.metric("Total Portfolio Value", f"${total_value:,.2f}")

    # Calculate Total PnL
    starting_portfolio_value = 100000  # Initial portfolio value
    total_pnl = total_value - starting_portfolio_value
    pnl_percentage = (total_pnl / starting_portfolio_value) * 100

    # Display Total PnL
    st.subheader("Total PnL")
    st.metric("Profit/Loss ($)", f"${total_pnl:,.2f}", delta=f"{pnl_percentage:.2f}%")

    # Calculate Performance Metrics
    total_trades = len(trade_history)
    win_rate = (trade_history["Signal"].str.contains("Buy") & (trade_history["Trade Amount"] > 0)).mean() * 100
    avg_trade_amount = trade_history["Trade Amount"].mean()
    max_trade = trade_history["Trade Amount"].max()
    min_trade = trade_history["Trade Amount"].min()

    # Display Performance Metrics
    st.subheader("Key Metrics")
    st.metric("Total Trades Executed", total_trades)
    st.metric("Win Rate", f"{win_rate:.2f}%")
    st.metric("Average Trade Amount", f"${avg_trade_amount:,.2f}")
    st.metric("Largest Trade", f"${max_trade:,.2f}")
