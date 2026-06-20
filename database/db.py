import sqlite3
from werkzeug.security import generate_password_hash


def get_db():
    conn = sqlite3.connect("spendly.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            email        TEXT    UNIQUE NOT NULL,
            password_hash TEXT   NOT NULL,
            created_at   TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        conn.close()
        return

    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 450.00,  "Food",          "2026-06-01", "Grocery run"),
        (user_id, 120.50,  "Transport",     "2026-06-03", "Metro card top-up"),
        (user_id, 1200.00, "Bills",         "2026-06-05", "Electricity bill"),
        (user_id, 350.00,  "Health",        "2026-06-08", "Pharmacy"),
        (user_id, 800.00,  "Entertainment", "2026-06-10", "OTT subscriptions"),
        (user_id, 2500.00, "Shopping",      "2026-06-13", "Clothes"),
        (user_id, 95.00,   "Other",         "2026-06-16", "Stationery"),
        (user_id, 220.00,  "Food",          "2026-06-19", "Restaurant dinner"),
    ]
    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()
