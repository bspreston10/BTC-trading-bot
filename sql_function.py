import sqlite3
from email_utils import send_email_signal_finalv5_news

def initialize_tables():
    conn = sqlite3.connect('trading_signals.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trading_signals_final (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            signal TEXT NOT NULL,
            entry_price DECIMAL(18, 8) NOT NULL,
            market_condition TEXT NOT NULL,
            buy_signal_count REAL NOT NULL,
            sell_signal_count REAL NOT NULL,
            symbol TEXT NOT NULL,
            UNIQUE (timestamp, symbol)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_sentiment_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            overall_sentiment_score REAL NOT NULL,
            sentiment_label TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized.")


def store_trading_signals(signal):

    """
    Store trading signals in the SQLite database.
    """
    try:
        conn = sqlite3.connect('trading_signals.db')
        cursor = conn.cursor()

        # Insert trading signals
        cursor.execute('''
            INSERT INTO trading_signals_final (timestamp, signal, entry_price, market_condition, buy_signal_count, sell_signal_count, symbol)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        ''', (
            signal['Timestamp'],
            signal['Signal'],
            signal['Entry Price'],
            signal['Market Condition'],
            signal['Buy Signal Count'],
            signal['Sell Signal Count'],
            signal['Symbol']
                       ))
        conn.commit()
        print("Trading signals stored successfully!")
    except Exception as e:
        print(f"Error storing trading signals: {e}")
    finally:
        conn.close()

def store_news_sentiment(timestamp, overall_score, overall_sentiment):
    try:
        conn = sqlite3.connect('trading_signals.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO news_sentiment_analysis (timestamp, overall_sentiment_score, sentiment_label)
                       VALUES(?, ?, ?)
        ''', (
            timestamp,
            overall_score,
            overall_sentiment
        ))
        conn.commit()
        print("News sentiment stored successfully!")
    except Exception as e:
        print(f"Error storing news sentiment: {e}")
    finally:
        conn.close()
        
        
def store_trading_signalsv2(signal):
    """
    Store trading signals in the SQLite database, avoiding duplicates.
    """
    try:
        conn = sqlite3.connect('trading_signals.db')
        cursor = conn.cursor()

        # Check if the row already exists
        cursor.execute('''
            SELECT 1 FROM trading_signals_final 
            WHERE timestamp = ? AND symbol = ?
        ''', (signal['Timestamp'], signal['Symbol']))

        if cursor.fetchone() is None:
            # Insert trading signals only if they don't exist
            cursor.execute('''
                INSERT INTO trading_signals_final (timestamp, signal, entry_price, market_condition, buy_signal_count, sell_signal_count, symbol)
                VALUES(?, ?, ?, ?, ?, ?, ?)
            ''', (
                signal['Timestamp'],
                signal['Signal'],
                signal['Entry Price'],
                signal['Market Condition'],
                signal['Buy Signal Count'],
                signal['Sell Signal Count'],
                signal['Symbol']
            ))
            conn.commit()
            print("Trading signal stored successfully!")
        else:
            print("Duplicate trading signal skipped:", signal)

    except Exception as e:
        print(f"Error storing trading signals: {e}")
    finally:
        conn.close()
