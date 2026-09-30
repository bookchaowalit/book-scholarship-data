# Upgrade plan — book-scholarship-data

Score: 6/10 -> 7.5/10 (pass 1) -> 7.5/10 (pass 2) — four GOV.UK sources had no parser tests, docs said fixtures-only; no CI.

## Backlog

- P0: Confirm the new GitHub Actions CI is green on the first push and keep it required.
- P1: Extract award amounts/dates from GOV.UK `details` parts instead of fixed unknowns.
- P1: Live-source monitoring (drift alerts) stays in the shared runtime; keep adapters pure.
- P2: Fill the PRODUCT.md acceptance-gate table only with evidence that exists (CI run link,
  replay report); do not mark gates passed without it.
- P2: Consider extracting the byte-identical `cli.py` shared by the sibling `book-*-data`
  products into one versioned package once a consumer exists (today each repo vendors it).

## Done in this pass (pass 1)

- Hardened: generic GOV.UK adapter now rejects a document whose `base_path` differs from the
  reviewed `fetch_url` path (misrouted/redirected content can no longer pass on markers alone).
- Added tests for all four GOV.UK sources (normalize, drift, misrouted path) and the Chevening
  closed-notice branch.
- PRODUCT.md/README: replaced "synthetic fixtures only" with the real five-source lineage and
  documented `schema-v2.json`.
- Added `.github/workflows/ci.yml`: Python 3.10/3.12 matrix, `pip install -e ".[dev]"`,
  `ruff check .`, `pytest`, and a `contract`/`validate`/`demo` CLI smoke. Verified by
  replaying those steps in a clean Python 3.10 venv.
- Added `[project.optional-dependencies] dev`, pytest config (`pythonpath = src`) and an
  explicit ruff rule set (E4/E9/F/I/B/UP); fixed the resulting import-order/encode lint.
- Added `tests/test_policy.py`: `sources.json` ↔ `source*.json` ↔ schema category
  consistency, duplicate policy copies identical, https/no-query URLs, 6h minimum
  interval, `--source-id` traversal rejection, capture fail-closed without
  `SOLO_EMPIRE_ROOT`, CLI `validate` exit codes without echoing input, bad demo clock.
- README: documented the developer/CI commands and offline test boundary.

## Done in this pass (pass 2)

- `contract --version {v1,v2}` (default v1, unchanged output) prints `schema-v2.json` for
  consumers of captured records; unknown versions exit 2. Tests cover both versions and
  that v2 matches the captured sources' `schema_version`; CI smoke and README updated.
- Drift guard: the HTML text extractor now also ignores `<noscript>` and `<svg>` (matching
  the sibling creator/deal/learning/mobility/paid-study/partnership/startup adapters), so
  markers hidden there cannot pass a challenge page; `tests/test_text_extraction.py`.
