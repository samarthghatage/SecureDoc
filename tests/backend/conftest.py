import pytest
from backend.app import create_app
from backend.database import init_db

@pytest.fixture()
def client(tmp_path):
    path=tmp_path/'test.sqlite3'; app=create_app({'TESTING':True,'DATABASE_PATH':path}); init_db(path)
    with app.test_client() as client: yield client
