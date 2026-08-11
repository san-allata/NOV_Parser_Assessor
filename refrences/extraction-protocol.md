# Deterministic Extraction Protocol (mandatory order of operations)

## Determinism settings
- Temperature 0. Fixed field order (A→ES). Stable, rule-based decisions only.
- Do NOT rely on relevance/top-k retrieval to establish presence of a field.

## Step 1 — Inventory & classify (exhaustive)
Enumerate EVERY file in the package. For each file, read EVERY page and tag it to a
document type (PO, COC, Dimension/Balloon, Hardness, NDT-UT, NDT-MPI, NDT-PT, NDT-vision-cert,
Coating, Light-band, Heat-treat, MTC, Concession, NCR, MWI). Sub-pages count individually —
a vision-cert page inside an NDT bundle is its own tagged page.

## Step 2 — Field sweep via anchor map
For each output field, go to its OWNING document (per field-anchor-map.md) and scan ALL
its pages for ALL anchor aliases (English + Chinese). Record for each field:
  value, source file, page, matched-anchor. If no anchor matches on any owned page →
  candidate NOT FOUND (must survive the gate in Step 4).

## Step 3 — Derive statuses via decision-rules.md
Apply R1–R7 mechanically. No discretion. Log which rule fired for each status.

## Step 4 — Completeness gate (HARD STOP — run scripts/completeness_gate.py)
Do not emit the row until the gate passes. The gate enforces:
  1. Every one of the 149 fields is populated (value, `NA`, or evidenced `NOT FOUND`).
  2. No `NOT FOUND` unless its owning-doc pages were logged as scanned in Step 2.
  3. No forbidden default: a raw-material NDT block may not be `Fail` when a passing
     finished-stage report of the same method exists (R2).
  4. No finished NDT `Check` caused ONLY by a missing eye-test date without a logged
     re-scan of the vision sub-pages.
  5. Dates stored as text; PO-line binding proven.
If the gate fails, return to Step 2 for the flagged fields and re-scan. Never override
the gate.

## Step 5 — Self-verification pass
Re-read every `NOT FOUND` and every `Check` once more against the anchor map. Only after
this second pass may the row be written.
