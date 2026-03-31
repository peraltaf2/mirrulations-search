# Ingesting Federal Register Documents for a Docket

## Prerequisites

`mirrulations-fetch` must be installed. From the repo root, run:

```bash
pip install -e /path/to/mirrulations-fetch
```

Your Postgres database must be running and reachable. The script reads connection info from a `.env` file or the standard `DATABASE_URL` / `PG*` environment variables. See `ingest_federal_registry_document.py` for details.

The `federal_register_documents` and `cfrparts` tables must exist. Run the schema if you haven't already:

```bash
psql $DATABASE_URL -f db/schema-postgres.sql
```

## Usage

Run from the repo root:

```bash
python3 db/ingest_fed_reg_docs_for_docket.py --docket-id OSHA-2025-0005
```

Replace `OSHA-2025-0005` with any valid regulations.gov docket ID.

## What the script does

1. Calls `mirrulations-fetch <docket-id> --no-comments` to download the docket from the mirrulations S3 bucket into `./<docket-id>/raw-data/`
2. Reads each `raw-data/documents/*.json` file and extracts the `frDocNum` field
3. For each unique FR document number, fetches the full document JSON from the Federal Register API (`federalregister.gov/api/v1/documents/<frDocNum>.json`)
4. Ingests each document into Postgres — populating the `federal_register_documents` and `cfrparts` tables

## Notes

- The downloaded docket folder (e.g. `./OSHA-2025-0005/`) is left in the current directory after the script finishes and can be deleted manually.
- The script can be run against an empty database — `federal_register_documents` and `cfrparts` have no foreign key dependencies on other tables.
- Documents not found in the Federal Register API are skipped with a warning and do not cause the script to fail.
- Running the script more than once for the same docket is safe — inserts use `ON CONFLICT ... DO UPDATE` / `DO NOTHING`.
