# NOV MRB Evaluation — deterministic operating procedure

You are producing one MRB result row (columns A–ES) per supplier package. Accuracy and
DETERMINISM are the priority: identical inputs must always produce the identical row.
"Incomplete extraction" is not an acceptable outcome — the procedure below is designed to
make missed values and ad-hoc status calls impossible to ship.

## MANDATORY: load these resources before you start, and follow them literally
1. `references/extraction-protocol.md` — the required order of operations (inventory →
   anchor sweep → derive → completeness gate → self-verify). Do NOT use relevance/top-k
   search to decide whether a field exists.
2. `references/field-anchor-map.md` — for every field, the owning document and the exact
   bilingual (English + Chinese) anchor strings to scan. A field may be `NOT FOUND` ONLY
   after every page of its owning document was scanned for every anchor alias.
3. `references/decision-rules.md` — R1–R7 status/applicability rules with fixed
   precedence. Apply mechanically; no discretion. Note especially R2 (raw-material NDT is
   `NA`, never `Fail`, when a passing finished-stage report of the same method exists on a
   non-weld part) and R3 (never downgrade a finished NDT block to `Check` for a missing
   eye-test date without a logged re-scan of the vision sub-pages).
4. `references/output-schema.md` — the AUTHORITATIVE 149-column A→ES layout: exact header
   order, header groups, sub-headers, the repeating 11-field NDT block layout, and the
   save-lock. This is the single source of truth for the workbook. Never reconstruct the
   column order from memory — follow this file exactly.

## Hard stop before emitting the row
Run `scripts/completeness_gate.py` (validate) with your row + scan_log + context.
If it raises, return to the anchor sweep for the flagged fields and re-scan. Never
override the gate, and never emit a row that has not passed it.

## Building the workbook
Generate the file with `scripts/build_row.py` (`build_workbook(values, path)`). It builds
the exact schema from `output-schema.md` and RAISES on any missing field, so column order
and completeness cannot drift by hand. Do NOT hand-assemble the column list in ad-hoc code.

## Output
- 149 columns A→ES, fixed order per `output-schema.md`. No blank cells: use a real value,
  `NA` (not applicable), or an evidenced `NOT FOUND`. Dates stored as text.
- Provide Section A (document inventory with file+page), Section B (PO-line binding with
  evidence), Section C (field table), then the workbook on request.
- Every `NOT FOUND` / `Check` must cite the pages actually scanned. Flag any single
  judgment call explicitly in Remarks so a reviewer can audit it.

## Self-check (last pass)
Re-read every `NOT FOUND` and every `Check` against the anchor map once more. Confirm the
Final Result follows R7, that no raw-material-NDT `NA` is being treated as a Reject driver,
and that the row satisfies every save-lock item in `output-schema.md`. Only then write it.
