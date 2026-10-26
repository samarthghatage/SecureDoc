# SecureDoc

SecureDoc is a local SHA-256 document integrity verification system. It stores document fingerprints in SQLite, compares later uploads against those references, records an audit history, and exports TXT/PDF reports. It does not store user documents after processing.

## Prerequisites

- Python 3.10+ and PowerShell
- Node.js 18+ and npm

## Run locally

From the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r backend\requirements.txt
cd frontend
npm install
cd ..
```

Open two PowerShell terminals. In the first:

```powershell
.\.venv\Scripts\Activate.ps1
py -m backend.app
```

In the second:

```powershell
cd frontend
npm run dev
```

Open http://127.0.0.1:5173. The API is available at http://127.0.0.1:5000/api. The database is initialized automatically under `data/`.

## Test and build

```powershell
py -m pytest -q
cd frontend
npm run build
```

The optional `start.ps1` helper checks prerequisites and opens both processes. Use `powershell -ExecutionPolicy Bypass -File .\start.ps1`.

## Features

- Register a document reference using a server-calculated SHA-256 hash.
- Verify unchanged and modified files, with explicit MATCH/MISMATCH results.
- Search and paginate document records and verification history.
- Export actual verification results as TXT or PDF.
- Dashboard statistics, activity chart, settings, and educational limitation notes.

Oversized uploads and file-processing failures return JSON errors and are not
written to verification history or converted into `MISMATCH` results.

## Architecture

`backend/` contains Flask routes, SQLite access, chunked hashing, validation, and reports. `frontend/src/` contains the React application shell, pages, design tokens, and central fetch service (the `api` function in `main.jsx`). Vite proxies `/api` to the local Flask server.

## Security and limitations

Uploads are written to generated temporary names, closed before processing, hashed in chunks, and removed after successful or failed processing. A 100 MB upload limit is enforced. The local SQLite reference is not tamper-proof if an attacker can alter both the document and its reference record. A matching hash proves content equality with the stored reference; it does not prove authorship.

For a beginner-friendly academic demo, SecureDoc intentionally has no login, cloud deployment, blockchain, or external key-management service.

## Troubleshooting

- If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process Bypass`.
- If the frontend cannot load data, confirm Flask is running on port 5000.
- If a port is busy, stop the existing process or change the backend `PORT` environment variable and the Vite proxy together.
