import sqlite3

DB_NAME = "data/medicine.db"


def connect():
    return sqlite3.connect(DB_NAME)


def search_medicine(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            b.brand_name,
            g.generic_name,
            g.indication,
            g.dose,
            g.side_effect,
            g.precaution,
            g.contra_indication,
            g.interaction,
            b.form,
            b.strength

        FROM brand b

        JOIN generic g
        ON b.generic_id = g.generic_id

        WHERE
            LOWER(b.brand_name) LIKE LOWER(?)
            OR LOWER(g.generic_name) LIKE LOWER(?)

        LIMIT 1
    """, (f"%{name}%", f"%{name}%"))

    result = cursor.fetchone()

    conn.close()

    return result


# ==========================
# Medicine History
# ==========================

def create_history_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_history(user_id, medicine_name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history(user_id, medicine_name)
        VALUES (?, ?)
    """, (user_id, medicine_name))

    conn.commit()
    conn.close()


def get_history(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT medicine_name, search_time
        FROM history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================
# Drug Interactions
# ==========================

def search_interaction(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            b.brand_name,
            g.interaction

        FROM brand b

        JOIN generic g
        ON b.generic_id = g.generic_id

        WHERE
            LOWER(b.brand_name) LIKE LOWER(?)
            OR LOWER(g.generic_name) LIKE LOWER(?)

        LIMIT 1
    """, (f"%{name}%", f"%{name}%"))

    result = cursor.fetchone()

    conn.close()

    return result


# ==========================
# Medication Reminder
# ==========================

def create_reminder_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


def save_reminder(user_id, medicine_name, reminder_time):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders (user_id, medicine_name, reminder_time)
        VALUES (?, ?, ?)
    """, (user_id, medicine_name, reminder_time))

    conn.commit()
    conn.close()


def get_active_reminders():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            medicine_name,
            reminder_time
        FROM reminders
        WHERE active = 1
    """)

    reminders = cursor.fetchall()

    conn.close()

    return reminders


def disable_reminder(reminder_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET active = 0
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()

# ==========================
# Clear History
# ==========================

def clear_history(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM history
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()
