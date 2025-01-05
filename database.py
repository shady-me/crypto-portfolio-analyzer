import sqlite3

def initialize_database():
    connection = sqlite3.connect("crypto_portfolio.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS portfolio (symbol TEXT, amount FLOAT, cost FLOAT)")
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()