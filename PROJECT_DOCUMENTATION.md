# SecureDoc — Academic Project Documentation

## Abstract

SecureDoc is a local web application that demonstrates document integrity checking with SHA-256. A user registers a reference fingerprint, later uploads a file, and receives a content comparison result with an audit record.

## Problem and objectives

Files can change without an obvious filename change. The project provides a beginner-friendly way to detect such changes, preserve verification history, and generate a report. The objectives are correct hashing, safe local uploads, clear UI feedback, and understandable documentation.

## Scope and requirements

The scope is local document registration and verification. It includes a React interface, Flask JSON API, SQLite persistence, search/filter/pagination, settings, and TXT/PDF exports. It does not include accounts, public deployment, or tamper-proof external key storage.

## Architecture and data flow

The browser sends a multipart upload to Flask. Flask writes a generated temporary file, hashes it in 1 MB chunks, compares or stores the digest, records the outcome in SQLite, removes the temporary file, and returns JSON. The browser renders the result and audit state.

Level 0 DFD: User → SecureDoc system → verification result/report.

Level 1 DFD: upload validation → SHA-256 module → document/reference database → comparison module → history database → UI/report response.

## Database design

`documents` stores filename, reference hash, size, MIME type, and timestamps. `verification_history` stores the document name, both hashes, result, file size, error field, and time. `settings` stores validated simple key/value preferences. Foreign keys use `ON DELETE SET NULL`, so deleting a reference does not erase history.

## Algorithms

SHA-256 is initialized, the file is read in 1 MB chunks, each chunk is added to the digest, and the final hexadecimal digest is stored or compared. Verification returns MATCH when the two digests are equal, otherwise MISMATCH.

## Testing plan and results

The six existing pytest tests pass (`6 passed`). They cover known/empty hashes,
registration, matching verification, modified content, history preservation after
deletion, and report generation. The final API review also verified the stored
digest, restart persistence, TXT/PDF report fields, the 100 MB rejection boundary,
missing-reference handling, and controlled file-processing errors. Run
`py -m pytest -q`. The frontend production check is `npm run build`.

Operational upload and processing failures return JSON errors (413 for an
oversized upload or 422 for a processing failure) and do not create history rows.
Temporary uploads use generated names, are closed before processing, and are
removed on successful and failed processing paths.

## Limitations and future scope

SQLite can be changed by an attacker who controls the workspace, so it is not tamper-proof. A future version could add signed references, user roles, or protected key storage, but those are intentionally outside this educational version.
