# SecureDoc API

All endpoints are local under `http://127.0.0.1:5000/api`. Errors return `{ "error": "message" }`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API status |
| GET | `/dashboard/stats` | Counts for registered documents and verification results |
| GET | `/dashboard/recent-activity` | Latest verification attempts |
| GET | `/dashboard/chart` | Daily match/mismatch totals |
| GET | `/documents?search=&page=&per_page=` | Search and paginate references |
| POST | `/documents/hash` | Multipart `file`; calculate hash without registration |
| POST | `/documents` | Multipart `file`; register reference |
| GET | `/documents/{id}` | Reference metadata |
| DELETE | `/documents/{id}` | Remove reference; history remains |
| POST | `/verify` | Multipart `document_id` and `file`; records comparison |
| GET | `/history?search=&result=&page=` | Search/filter verification audit trail |
| GET | `/history/{id}` | Full verification record |
| GET | `/reports/verification/{id}?format=txt\|pdf` | Download an actual report |
| GET/PUT | `/settings` | Read or update local settings |

`MATCH` means the calculated SHA-256 equals the stored reference. `MISMATCH` means the contents differ. A missing reference returns `404`; an oversized upload returns `413`; and a file-processing failure returns `422`. These operational failures are not recorded as mismatches or history rows. SQL filters use bound parameters, and document sorting is restricted to a fixed allow-list.
