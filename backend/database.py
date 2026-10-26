import sqlite3
from .config import DATABASE_PATH, ensure_directories

SCHEMA = '''
CREATE TABLE IF NOT EXISTS documents (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, reference_hash TEXT NOT NULL,
 size_bytes INTEGER NOT NULL DEFAULT 0, mime_type TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS verification_history (
 id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER, document_name TEXT NOT NULL,
 reference_hash TEXT, calculated_hash TEXT, result TEXT NOT NULL, file_size INTEGER,
 error_message TEXT, verified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS settings (
 key TEXT PRIMARY KEY, value TEXT NOT NULL
);
'''

def get_db(path=None):
    ensure_directories()
    conn = sqlite3.connect(path or DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db(path=None):
    conn = get_db(path)
    conn.executescript(SCHEMA)
    defaults = {'app_name': 'SecureDoc', 'max_upload_mb': '100', 'retention_days': '365'}
    for key, value in defaults.items():
        conn.execute('INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)', (key, value))
    conn.commit(); conn.close()
