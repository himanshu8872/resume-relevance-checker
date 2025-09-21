import sqlite3

def init_db():
    """
    Initializes the SQLite database and creates the necessary tables if they don't exist.
    """
    conn = sqlite3.connect('hackathon.db')
    cursor = conn.cursor()

    # Create Jobs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        description_text TEXT NOT NULL
    )
    ''')

    # Create Resumes Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_name TEXT NOT NULL,
        email TEXT,
        text_content TEXT NOT NULL
    )
    ''')

    # Create Evaluations Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_id INTEGER,
        job_id INTEGER,
        score REAL,
        verdict TEXT,
        analysis_text TEXT,
        FOREIGN KEY(resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
        FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()