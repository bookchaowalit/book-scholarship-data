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

## Done in this pass (pass 3)

- Score: 7.5 -> 8.
- Chevening "until <date>, at HH:MM (UTC)" is parsed with an explicit month table (no locale-dependent `strptime(%B)`), and a naive `checked_at` raises ValueError instead of TypeError; tests cover the cutoff at UTC, +07:00 and -04:00.
- Shared `cli.py` (same edit in all 13 sibling copies): `validate` now rejects NaN, ±Infinity and overflowing literals such as `1e400` (Python's json turns them into non-finite floats that JSON Schema `number` accepted); `timestamp` normalises fractional seconds so Python 3.10 accepts the same RFC3339 values as 3.11+ (it rejected e.g. `.1Z`) and only ASCII digits match; a trailing-dot `example.org.` host can no longer be claimed `live`.
- `tests/test_shared_cli.py` (byte-identical in all 13 repos) pins this repo's `cli.py` sha256 (three variants: base, +`contract --version`, +benefit availability) so a one-repo edit fails CI, and covers the fixes above across UTC/+07:00/-04:00 offsets. To change `cli.py`: edit every copy of the variant, then update `CLI_SHA256` in all 13 copies of the test.
- Not done (needs a reviewed live capture, so left blocked): stronger drift markers and any page-phrase extraction; no page phrases were invented.
