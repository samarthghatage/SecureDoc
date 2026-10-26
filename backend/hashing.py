import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024

def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(path, 'rb') as file:
        while chunk := file.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()

def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
