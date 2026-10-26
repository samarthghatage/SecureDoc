import hashlib
from backend.hashing import sha256_bytes

def test_known_input(): assert sha256_bytes(b'SecureDoc') == hashlib.sha256(b'SecureDoc').hexdigest()
def test_empty_input(): assert sha256_bytes(b'') == hashlib.sha256(b'').hexdigest()
