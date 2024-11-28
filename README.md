# BTC-trading-bot
Automated trading bot for Bitcoin that generates buy/sell signals

## Table of Contents
- [Project Objective](#project-objective)
- [Data Collection](#data-collection)
- [Strategy Creation](#strategy-creation)
- [Sentiment Analysis](#sentiment-analysis)
- [SQL Database Integration](#sql-database-integration)
- [Next Steps](#next-steps)



## Email Generated

<img width="245" alt="Screenshot 2024-11-27 at 1 02 11 AM" src="https://github.com/user-attachments/assets/6c08e658-3640-4996-8bc8-9784ff6fa7b2">      <img width="886" alt="Screenshot 2024-11-27 at 1 03 12 AM" src="https://github.com/user-attachments/assets/5951e39b-38df-48e2-ae44-a3de39df84e0">



## Project Objective
This project involved designing an automated trading bot focused on Bitcoin (BTC) and Dogecoin (DOGE). The bot provides real-time buy/sell recommendations by analyzing market data and sends trading signals via email at the start of every hour.
### Why Would I pick these stocks?
Bitcoin and Dogecoin were selected due to their prominence in the cryptocurrency market, high trading volumes, and accessibility for retail traders. By focusing on these assets, the bot demonstrates its ability to operate in diverse market conditions, ranging from high-stability assets like Bitcoin to more volatile ones like Dogecoin.
### Future Business Strategy
While the bot’s trading recommendations aim to generate profit, the long-term strategy focuses on scalability through a subscription-based email service. This model offers a consistent revenue stream independent of market performance, making it a more sustainable and attractive business proposition. Subscribers would benefit from:
- Regular, expert-driven trading insights.
- Transparency and reliability in market analysis.
- Potential expansions into other cryptocurrencies or markets.

By shifting the focus from proprietary trading to a service-based model, this project highlights its potential to scale as a business while reducing financial risk.

# Creation of Bot
## Data Collection
I started out by just focusing on Bitcoin (BTC/USDT). For my training data, I collected 1 hour candlestick movement using the binnance API from the ccxt library. To ensure that the strategy would work in multiple markets I grabbed data from a time period where Bitcoin was trending heavily, and I grabbed data from a time where Bitcoin was in a sideways market.

<img width="515" alt="Screenshot 2024-11-26 at 3 13 54 PM" src="https://github.com/user-attachments/assets/fdb028c8-8d89-47d2-ad7b-381fd496a02e">


For DOGE (DOGE/USDT) the only reason I started using this data was I wanted to see how my strategy would work on a coin with a much smaller market cap and value. Analysis for this coin is less strict due to the model mainly being trained on Bitcoin data.

<img width="475" alt="Screenshot 2024-11-26 at 3 15 31 PM" src="https://github.com/user-attachments/assets/0f4dc404-4fe2-43cb-a3e1-bbf197686a1a">

## Strategy Creation
I leverage a variety of technical indicators to identify trends, momentum, and potential reversal points. These include:
- **MACD (Moving Average Convergence Divergence):** For detecting momentum and trend direction shifts
- **EMA (Exponential Moving Average):** To emphasize recent price movements and quickly adapts to changing market conditions
- **Bollinger Bands:** To measure volatility and overbought/oversold conditions
- **RSI (Relative Strength Index):** For gauging the strength of price movements and spotting potential reversals

Combining these metrics and optimizing the hyperparameters I was able to achieve these success metrics in backtesting:

<img width="191" alt="Screenshot 2024-11-27 at 12 46 33 AM" src="https://github.com/user-attachments/assets/3403eeb5-3404-411e-bdfd-995f01ad903d">

#### Sentiment Analysis
Bitcoin, and crypto in general, is known to be highly reactive to news event that can trigger massive spikes in price. To combat this, I decided to run an API that fetchs news relating to Bitcoin and crypto in general, and then I implement a Natural Language Processing tool to analyze key words in the data and labels it "Bullish", "Bearish", or "Nuetral" and gives it a score based on the probability that it is that label.

<img width="1019" alt="Screenshot 2024-11-27 at 1 00 27 AM" src="https://github.com/user-attachments/assets/cd63c1c9-20f2-448f-ae5c-71656a33e744">

## SQL Database Integration
<img width="842" alt="Screenshot 2024-11-27 at 8 26 00 PM" src="https://github.com/user-attachments/assets/fd8122f5-0147-46bf-823e-810b0e26c6f9">

Each time an email is sent, the trading signal and its associated metadata—such as timestamps, market conditions, and entry prices—are seamlessly stored in a structured SQL table. This table is designed to automatically update with every new signal, ensuring the accurate and timely capture of critical data for analysis and decision-making.

## Implementing the Model on a Live Market
After comnfirming that the model performs well during backtesting, I decided it was time to run it against the live market to see how it detects trading signals live. After running the bot periodically for a little over a week, I achieved the metrics below:

<img width="415" alt="Screenshot 2024-11-27 at 10 43 30 AM" src="https://github.com/user-attachments/assets/8a71d3af-198e-4de3-a4d7-6dbb75fca946">

<img width="208" alt="Screenshot 2024-11-27 at 10 43 06 AM" src="https://github.com/user-attachments/assets/ca2bcdef-89e4-4c3f-acef-b77c44aece18">

## Next Steps
Due to the performance of the metrics observed, I deemed it appropriate to implement a portfolio management system within the code. This system autonomously executes buy and sell actions for the cryptocurrencies based on the trading signals provided in the email alerts. Each trade, along with its relevant details, is logged in a structured CSV file to ensure complete transparency and traceability. Over time, this logged data will be thoroughly reviewed and analyzed to evaluate how the strategy performs in a live market environment. The insights gained will provide a clearer understanding of profit trends and areas for potential refinement, bringing the project closer to real-world application and optimization

I am currently focused on analyzing blockchain activity data to explore its potential in providing deeper insights into predicting Bitcoin price movements. By examining metrics such as transaction volumes, unique addresses, and other on-chain indicators, I aim to uncover patterns and correlations that could enhance the accuracy of price movement predictions.
