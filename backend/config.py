from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv('SECUREDOC_DATA_DIR', ROOT / 'data'))
REPORTS_DIR = Path(os.getenv('SECUREDOC_REPORTS_DIR', ROOT / 'reports'))
DATABASE_PATH = Path(os.getenv('SECUREDOC_DATABASE', DATA_DIR / 'securedoc.sqlite3'))
MAX_UPLOAD_BYTES = int(os.getenv('SECUREDOC_MAX_UPLOAD_BYTES', 100 * 1024 * 1024))

def ensure_directories():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
