import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# Database connection function
def get_db_connection():
    return sqlite3.connect("portfolio.db")

# Fetch data from the database
def fetch_cash():
    conn = get_db_connection()
    cash_query = "SELECT cash FROM portfolio_cash LIMIT 1"
    cash = pd.read_sql_query(cash_query, conn).iloc[0, 0]
    conn.close()
    return cash

def fetch_positions():
    conn = get_db_connection()
    positions_query = """
        SELECT symbol, quantity, entry_price, take_profit_price, stop_loss_price 
        FROM portfolio_summary
    """
    positions_df = pd.read_sql_query(positions_query, conn)
    conn.close()
    return positions_df

def load_trade_history():
    trade_history_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simulated_trades_log.csv")
    if os.path.exists(trade_history_path):
        trade_history = pd.read_csv(trade_history_path)
        trade_history["Timestamp"] = pd.to_datetime(trade_history["Timestamp"])
        trade_history["Entry Price"] = pd.to_numeric(trade_history["Entry Price"], errors="coerce")
        trade_history["Trade Amount"] = pd.to_numeric(trade_history["Trade Amount"], errors="coerce")
        trade_history.dropna(inplace=True)
        trade_history["Trade Type"] = trade_history["Signal"].str.contains("Buy").map({True: "Buy", False: "Sell"})
        return trade_history
    else:
        st.warning("Trade history file not found!")
        return pd.DataFrame()

# Streamlit App
st.title("Trading Bot Dashboard")
st.sidebar.header("Filters & Navigation")

# Sidebar navigation
tabs = st.sidebar.radio("Go to:", ["Portfolio Summary", "Trade History", "Performance Metrics"])

# Dynamically fetch data for the current tab
if tabs == "Portfolio Summary":
    st.header("Portfolio Summary")

    # Fetch and display cash dynamically
    cash = fetch_cash()
    st.metric("Cash Available", f"${cash:,.2f}")

    # Fetch and display positions dynamically
    positions_df = fetch_positions()
    positions_df["Total Value"] = positions_df["quantity"] * positions_df["entry_price"]

    st.subheader("Open Positions")
    st.dataframe(positions_df)

    st.subheader("Portfolio Allocation")
    fig, ax = plt.subplots()
    positions_df.set_index("symbol")["Total Value"].plot(kind="bar", ax=ax, color="skyblue")
    ax.set_title("Portfolio Value by Asset")
    ax.set_ylabel("Value ($)")
    ax.set_xlabel("Asset")
    st.pyplot(fig)

elif tabs == "Trade History":
    st.header("Trade History")

    # Fetch trade history dynamically
    trade_history = load_trade_history()

    if not trade_history.empty:
        st.subheader("All Trades")
        st.dataframe(trade_history)

        st.subheader("Filter Trades by Asset")
        selected_asset = st.selectbox("Select an Asset", trade_history["Symbol"].unique())
        filtered_trades = trade_history[trade_history["Symbol"] == selected_asset]
        st.write(f"Showing trades for: {selected_asset}")
        st.dataframe(filtered_trades)
    else:
        st.write("No trade history available.")

elif tabs == "Performance Metrics":
    st.header("Performance Metrics")

    # Fetch cash and positions dynamically
    cash = fetch_cash()
    positions_df = fetch_positions()
    positions_df["Total Value"] = positions_df["quantity"] * positions_df["entry_price"]

    # Total portfolio value
    total_value = cash + positions_df["Total Value"].sum()
    st.metric("Total Portfolio Value", f"${total_value:,.2f}")

    # Calculate total PnL
    starting_portfolio_value = 100000
    total_pnl = total_value - starting_portfolio_value
    pnl_percentage = (total_pnl / starting_portfolio_value) * 100

    st.subheader("Total PnL")
    st.metric("Profit/Loss ($)", f"${total_pnl:,.2f}", delta=f"{pnl_percentage:.2f}%")

    # Display performance metrics
    trade_history = load_trade_history()
    if not trade_history.empty:
        total_trades = len(trade_history)
        win_rate = (trade_history["Signal"].str.contains("Buy") & (trade_history["Trade Amount"] > 0)).mean() * 100
        avg_trade_amount = trade_history["Trade Amount"].mean()
        max_trade = trade_history["Trade Amount"].max()
        min_trade = trade_history["Trade Amount"].min()

        st.subheader("Key Metrics")
        st.metric("Total Trades Executed", total_trades)
        st.metric("Win Rate", f"{win_rate:.2f}%")
        st.metric("Average Trade Amount", f"${avg_trade_amount:,.2f}")
        st.metric("Largest Trade", f"${max_trade:,.2f}")
