import sqlite3

DATABASE_PATH = 'savings.db'
def init_db(starting_amount=2400):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS total_savings (total_amount INTEGER)''')
    cursor.execute('INSERT INTO total_savings (total_amount) SELECT ? WHERE NOT EXISTS (SELECT 1 FROM total_savings)', (starting_amount,))
    conn.commit()
    conn.close()

def get_total_savings():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT total_amount FROM total_savings")
    total_saved = cursor.fetchone()[0]
    conn.close()
    return total_saved

def update_total_savings(amount):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE total_savings SET total_amount = total_amount + ?", (amount,))
    conn.commit()
    conn.close()
