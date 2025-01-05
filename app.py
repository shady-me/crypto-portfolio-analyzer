import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    conn = sqlite3.connect('crypto_portfolio.db')
    return conn

def add_coin(symbol, amount, cost):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO portfolio (symbol, amount, cost) VALUES (?, ?, ?)", (symbol, amount, cost))
    conn.commit()
    conn.close()

def view_portfolio():
    conn = get_connection()
    df = pd.read_sql('SELECT symbol, amount, cost FROM portfolio', conn)
    conn.close()
    return df

def delete_coin(symbol):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM portfolio WHERE symbol=?", (symbol,))
    conn.commit()
    conn.close()

def data_entry_page():
    st.subheader("Add or Update Coin")
    with st.form("add_coin_form"):
        symbol = st.text_input("Coin Symbol (e.g., BTC, ETH)")
        amount = st.number_input("Amount", min_value=0.0, format="%.8f")
        cost = st.number_input("Cost", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Add or Update Coin")

        if submitted:
            if symbol.strip() == "":
                st.error("Symbol cannot be blank!")
            else:
                add_coin(symbol, amount, cost)
                st.success("Coin added to or updated in portfolio")

    st.subheader("Delete a Coin")
    delete_symbol = st.text_input("Enter the symbol of the coin to delete")
    if st.button("Delete Coin"):
        if delete_symbol.strip() == "":
            st.error("Symbol cannot be blank!")
        else:
            delete_coin(delete_symbol)
            st.success("Coin deleted from portfolio")

def portfolio_page():
    st.subheader("Your Portfolio")
    df = view_portfolio()
    st.table(df)

# Main app layout
st.title("Cryptocurrency Portfolio Tracker")
tab1, tab2 = st.tabs(["Portfolio", "Data Entry"])

with tab1:
    portfolio_page()
with tab2:
    data_entry_page()