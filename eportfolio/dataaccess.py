import sqlite3
import traceback
import logging

DATABASE = 'eportfolio.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()
    logging.debug("Initializing database...")

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL);''')
    logging.debug("Created users table if not exists.")

    cur.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        subjectname TEXT NOT NULL,
        teacher_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES users (id),
        FOREIGN KEY (student_id) REFERENCES users (id));''')
    logging.debug("Created subjects table if not exists.")

    cur.execute('''CREATE TABLE IF NOT EXISTS portfolios (
        id INTEGER PRIMARY KEY,
        subject_id INTEGER,
        user_id INTEGER,
        entry TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects (id),
        FOREIGN KEY (user_id) REFERENCES users (id));''')
    logging.debug("Created portfolios table if not exists.")

    conn.commit()
    conn.close()
    logging.debug("Database initialization complete.")

def add_user(username, password, role):
    query = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (username, password, role))
        conn.commit()
        logging.debug(f"User {username} added successfully.")
        return cur.lastrowid
    except Exception as e:
        logging.error(f"Error adding user: {e}")
        traceback.print_exc()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_subject(subjectname, teacher_id, student_id):
    query = "INSERT INTO subjects (subjectname, teacher_id, student_id) VALUES (?, ?, ?)"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (subjectname, teacher_id, student_id))
        conn.commit()
        logging.debug(f"Subject {subjectname} added successfully.")
        return cur.lastrowid
    except Exception as e:
        logging.error(f"Error adding subject: {e}")
        traceback.print_exc()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_subjects(user_id, search_term):
    query = "SELECT * FROM subjects WHERE (teacher_id = ? OR student_id = ?) AND subjectname LIKE ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id, user_id, f'%{search_term}%'))
        subjects = cur.fetchall()
        logging.debug(f"Subjects found: {subjects}")
        return subjects
    except Exception as e:
        logging.error(f"Error fetching subjects: {e}")
        traceback.print_exc()
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def add_portfolio_entry(subject_id, user_id, entry):
    logging.debug(f"Attempting to add entry for subject_id: {subject_id}, user_id: {user_id}, entry: {entry}")
    query = "INSERT INTO portfolios (subject_id, user_id, entry) VALUES (?, ?, ?)"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (subject_id, user_id, entry))
        conn.commit()
        logging.debug("Portfolio entry added successfully.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        traceback.print_exc()
    except Exception as e:
        logging.error(f"Exception in add_portfolio_entry: {e}")
        traceback.print_exc()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_portfolio_entries(subject_id):
    query = "SELECT * FROM portfolios WHERE subject_id = ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (subject_id,))
        entries = cur.fetchall()
        logging.debug(f"Portfolio entries retrieved: {entries}")
        return entries
    except Exception as e:
        logging.error(f"Error fetching portfolio entries: {e}")
        traceback.print_exc()
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def validate_user(username, password):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (username, password))
        user = cur.fetchone()
        logging.debug(f"User validation result: {user}")
        return user
    except Exception as e:
        logging.error(f"Error validating user: {e}")
        traceback.print_exc()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (username,))
        user = cur.fetchone()
        logging.debug(f"User search result: {user}")
        return user
    except Exception as e:
        logging.error(f"Error searching user: {e}")
        traceback.print_exc()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        logging.debug(f"User search by id result: {user}")
        return user
    except Exception as e:
        logging.error(f"Error searching user by id: {e}")
        traceback.print_exc()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_subject_by_id(subject_id):
    query = "SELECT * FROM subjects WHERE id = ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (subject_id,))
        subject = cur.fetchone()
        logging.debug(f"Subject search by id result: {subject}")
        return subject
    except Exception as e:
        logging.error(f"Error searching subject by id: {e}")
        traceback.print_exc()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_reports_by_user_id(user_id):
    query = "SELECT * FROM portfolios WHERE user_id = ?"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        reports = cur.fetchall()
        logging.debug(f"Reports search by user id result: {reports}")
        return reports
    except Exception as e:
        logging.error(f"Error searching reports by user id: {e}")
        traceback.print_exc()
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    class User:
        def __init__(self, username, password, role):
            self.username = username
            self.password = password
            self.role = role

    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Creating tables...")
    initialize_db()
    logging.debug("Database created successfully.")

    sample_users = [
        User(username="admin", password="password", role="admin"),
        User(username="user", password="password", role="user"),
        User(username="teacher", password="password", role="teacher")
    ]
    
    for user in sample_users:
        result = add_user(user.username, user.password, user.role)
        if result:
            logging.debug(f"Added user: {user.username}")

    logging.debug("Validating user 'admin' with password 'password':")
    logging.debug(validate_user("admin", "password"))

    user = search_user("admin")
    if user:
        logging.debug(f"Searched user 'admin': {dict(user)}")
        subject_id = add_subject("Mathematics", user['id'], None)
        if subject_id:
            logging.debug(f"Added subject 'Mathematics' with ID: {subject_id}")

        subjects = search_subjects(user['id'], "")
        for subject in subjects:
            logging.debug(f"Subject found: {dict(subject)}")

    user_by_id = search_user_by_id(1)
    if user_by_id:
        logging.debug(f"Search user by ID 1: {dict(user_by_id)}")

    subject_by_id = search_subject_by_id(1)
    if subject_by_id:
        logging.debug(f"Search subject by ID 1: {dict(subject_by_id)}")
    else:
        logging.debug("No subject found with ID 1")

    reports = search_reports_by_user_id(1)
    for report in reports:
        logging.debug(f"Report found: {dict(report)}")