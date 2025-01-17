import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON Data
with open("/Users/bennett/Desktop/trading_bot/portfolio.json", "r") as f:
    portfolio = json.load(f)

# Extract Portfolio Details
cash = portfolio["cash"]
positions = portfolio["positions"]

# Convert Positions to DataFrame
positions_df = pd.DataFrame(positions).T
positions_df["Total Value"] = (
    positions_df["quantity"] * positions_df["entry_price"]
)

# Streamlit App
st.title("Trading Bot Dashboard")
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
ax.set_title("Total Value by Asset")
ax.set_ylabel("Value ($)")
ax.set_xlabel("Asset")
st.pyplot(fig)

st.write("Data source: `portfolio.json`")