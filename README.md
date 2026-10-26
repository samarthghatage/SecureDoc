# SecureDoc — Document Integrity Verification System

SecureDoc is a local, web-based document integrity verification system that uses **SHA-256 cryptographic hashing** to detect changes in files. It stores document reference hashes in an SQLite database, compares uploaded files against registered references, maintains a verification history, and generates TXT/PDF verification reports.

The application is designed as a beginner-friendly academic project demonstrating document integrity verification using a React frontend and Python Flask backend.

> **Important:** SecureDoc verifies file-content integrity against a stored reference. It does not prove document authorship, and hashing is not encryption.

## Features

- **Document Registration:** Register documents and generate SHA-256 reference hashes.
- **Integrity Verification:** Compare uploaded files against registered references.
- **Match Detection:** Identify files whose SHA-256 hashes match their stored references.
- **Mismatch Detection:** Identify files whose contents differ from their registered references.
- **Verification History:** Maintain a record of verification attempts and their results.
- **Document Management:** Search, sort, and paginate registered document records.
- **Dashboard:** View document statistics, successful verifications, failed verifications, and activity.
- **Report Export:** Generate TXT and PDF verification reports containing relevant verification details.
- **Input Validation:** Handle invalid inputs, missing references, oversized uploads, and file-processing errors.
- **Temporary File Cleanup:** Remove temporary uploaded files after processing.
- **Local Storage:** Store reference records and verification history in SQLite.
- **Responsive Interface:** Use the application through a modern web interface.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | Python, Flask |
| Database | SQLite |
| Cryptographic Hashing | SHA-256 using Python `hashlib` |
| Charts | Recharts |
| Icons | Lucide React |
| Report Generation | TXT and PDF export |

## Architecture

SecureDoc uses a client-server architecture running locally.

```text
                 SecureDoc
                     |
          +----------+----------+
          |                     |
     React Frontend         Flask Backend
       (Vite)                    |
          |           +----------+----------+
          |           |          |          |
          +---------->|  Hashing  | SQLite   |
                      |  SHA-256 | Database |
                      +----------+----------+
                                 |
                          TXT/PDF Reports
```

### How it works

1. **Register a document:** The backend reads the file and calculates its SHA-256 hash.
2. **Store the reference:** The document's reference information and hash are saved in SQLite.
3. **Verify a document:** The backend calculates the SHA-256 hash of the submitted file.
4. **Compare hashes:** The calculated hash is compared with the registered reference hash.
5. **Record the result:** The verification outcome is recorded in the history when appropriate.
6. **Export a report:** The application generates a TXT or PDF report containing the verification details.

A `MATCH` result indicates that the file's content matches the registered reference at the byte level. A `MISMATCH` result indicates that the calculated hash differs from the stored reference hash.

## Prerequisites

Install the following software before running SecureDoc:

- **Python 3.10 or later**
- **Node.js 18 or later**
- **npm**
- **Git** (optional, for cloning the repository)
- **PowerShell** (for the Windows commands below)

Check your installed versions:

```powershell
python --version
node --version
npm --version
```

## Installation and Setup

### 1. Clone the repository

If you are downloading the project from GitHub, run:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SecureDoc
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository's actual clone URL.

Alternatively, download the repository ZIP from GitHub and extract it.

### 2. Create a Python virtual environment

Run these commands from the project root:

```powershell
py -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

From the project root, run:

```powershell
py -m pip install -r backend\requirements.txt
```

### 4. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

## Run SecureDoc Locally

Start the backend and frontend in **two separate PowerShell terminals**.

### Terminal 1 — Backend

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1
py -m backend.app
```

The Flask backend runs at:

`http://127.0.0.1:5000`

The API is available under:

`http://127.0.0.1:5000/api`

### Terminal 2 — Frontend

From the project root:

```powershell
cd frontend
npm run dev
```

Open the application in your browser:

**http://127.0.0.1:5173**

The SQLite database is initialized automatically under the project's `data/` directory, according to the application's configuration.

### Optional startup script

If the repository includes `start.ps1`, you can use the helper script to start the application:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

## Testing and Production Build

### Run backend tests

From the project root, activate the virtual environment and run:

```powershell
.\.venv\Scripts\Activate.ps1
py -m pytest -q
```

### Build the frontend

```powershell
cd frontend
npm run build
```

The production build is generated according to the Vite configuration.

### Recommended manual tests

After starting SecureDoc, test these scenarios:

| Test | Action | Expected result |
|---|---|---|
| Registration | Register a new document | A SHA-256 reference hash is generated and stored |
| Successful verification | Verify the unchanged document | `MATCH` |
| Modified document | Modify the registered document and verify it | `MISMATCH` |
| Missing reference | Verify a document without a registered reference | Reference-not-found response, not a false mismatch |
| Verification history | Perform successful and unsuccessful checks | Appropriate verification events appear |
| TXT report | Export a verification report | A readable TXT report is generated |
| PDF report | Export a verification report | A readable PDF report is generated |
| Persistence | Restart the application | Stored SQLite records remain available |
| Upload size | Upload a file exceeding the configured limit | The upload is rejected |
| Error handling | Trigger a safe processing failure | A clear error is returned without a false mismatch entry |

For additional edge cases and detailed instructions, consult `TEST_PLAN.md` if it is included in your local test pack.

## API and Error Handling

The Flask backend provides the application's API for registration, verification, document records, history, dashboard statistics, and reports.

The exact endpoints and request formats are defined by the implementation in `backend/` and should be documented in `API_DOCUMENTATION.md` if that file is included in the repository.

Reported error-handling behavior includes:

- Missing references return an appropriate not-found response.
- File-processing failures return JSON errors rather than being treated as mismatches.
- Oversized uploads are rejected.
- Invalid pagination values are handled without unhandled server errors.
- Processing failures should not create false `MISMATCH` history entries.
- Temporary uploads are cleaned up after processing.

Consult the API documentation and implementation for exact status codes and response formats.

## Project Structure

The project follows this general structure:

```text
SecureDoc/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── hashing.py
│   ├── documents.py
│   ├── verification.py
│   ├── history.py
│   ├── reports.py
│   ├── validators.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── data/
├── reports/
├── tests/
├── README.md
├── PROJECT_DOCUMENTATION.md
├── API_DOCUMENTATION.md
└── start.ps1
```

The exact files and folders may differ slightly depending on the final repository contents.

## Security and Limitations

### SHA-256 hashing

SecureDoc uses SHA-256 to calculate a fingerprint of a file's bytes. Changing the file content normally produces a different hash.

### Hashing is not encryption

Hashing does not encrypt a document or make its contents secret. SecureDoc uses hashes for integrity comparison, not confidentiality.

### A matching hash does not prove authorship

A `MATCH` result indicates that the calculated hash matches the stored reference. It does not establish who created, signed, or authorized the document.

### Local database limitations

The SQLite database stores the trusted reference hashes locally. If an attacker can modify both a document and its stored reference record, the database alone cannot guarantee tamper-proof verification.

### File handling

Uploads are processed locally by the application. Temporary files are intended to be removed after processing, and the application enforces a reported upload limit of 100 MiB.

Do not upload sensitive or confidential documents unless you have reviewed the application's deployment, storage, logging, and security configuration.

### Intended use

SecureDoc is designed for learning, demonstration, and academic purposes. It does not currently provide enterprise-grade authentication, cloud storage, external key management, digital signatures, or an independently protected audit ledger.

## Troubleshooting

### PowerShell cannot activate the virtual environment

Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### Frontend cannot connect to the backend

Confirm that Flask is running at:

`http://127.0.0.1:5000`

Then restart the frontend if necessary.

### Port 5000 is already in use

Stop the existing process or configure a different backend port. If you change the backend port, update the Vite API proxy configuration to match.

### Frontend dependencies are missing

From the frontend directory, run:

```powershell
npm install
```

### Backend dependencies are missing

From the project root, activate the virtual environment and run:

```powershell
py -m pip install -r backend\requirements.txt
```

### Database or application startup issues

Check the terminal output for the actual error. Confirm that the application has permission to create or access its configured data directory.

## Future Improvements

Potential future improvements include:

- Automated browser-based end-to-end testing.
- More comprehensive automated API tests.
- Improved audit-log protection.
- Stronger protection for trusted reference hashes.
- Additional accessibility and responsive-layout testing.

## Author

Developed as an academic project to demonstrate document integrity verification using SHA-256 hashing, Python Flask, React, and SQLite.