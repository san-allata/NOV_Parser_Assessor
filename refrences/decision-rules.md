# Deterministic Decision Rules (no discretion permitted)

These rules are absolute. Identical inputs MUST yield identical output. Where a rule
says NA or Check, you may NOT substitute Fail.

## R1 — NDT stage classification (Material vs Finished)
Determine stage from the report's OWN evidence, in this precedence:
1. Ticked checkbox: "成品/Finished Machined" → FINISHED; "毛坯/Raw Material" → MATERIAL.
2. Surface Condition: "车铣/Machined/Final Machining" → FINISHED; "as-forged/mill" → MATERIAL.
3. Explicit title words. 4. If bound to the final-inspection dimensional set → FINISHED.
A single method's report populates exactly ONE stage (max populated stage count = 1).

## R2 — Raw-material NDT block = NA, NOT Fail  (THE UT-MATERIAL RULE)
A raw-material NDT block (MPI/LPI/UT/RT Material) is `NA` when BOTH:
  (a) the part is non-weld / non-overlay (per MWI + description), AND
  (b) a passing FINISHED-stage report of the SAME method exists in the package.
→ In that case the single finished-stage report SATISFIES the method requirement.
FORBIDDEN: marking a raw-material NDT block `Fail` solely because only a finished-stage
report exists. Raw-material NDT is `Fail` ONLY if a governing doc EXPLICITLY mandates a
SEPARATE raw-material examination AND it is absent.
If applicability genuinely cannot be resolved → `Check` (never `Fail`).

## R3 — Finished NDT block status
`Pass` when ALL: report present + accepted qty = inspected qty (0 rejected) + valid
operator qualification + eye-test date present. If only the eye-test date is missing →
re-scan the vision sub-pages (see field-anchor-map) BEFORE downgrading. Downgrade to
`Check` only after an evidenced exhaustive scan fails. Never `Fail` for a missing admin
date alone.

## R4 — Surface Finish (Column AB, Yes/No only)
Gate: check DRAWING first, then MWI surface-finish/roughness cell.
- No requirement anywhere → `No` (not applicable; no remark, no Fail).
- Requirement exists + valid measured evidence (roughness report, light-band report, or
  Ra values on dimensional/NDT reports) → `Yes`.
- Requirement exists + evidence missing/unreadable → `No`.

## R5 — Finished UT/RT applicability
Applicable ONLY for weld / inlay / overlay parts. For a plain forging with a single
volumetric UT on the finished part, that UT is the Finished-UT block; RT stays `NA`
unless the part is welded/clad.

## R6 — NA vs "-" vs NOT FOUND notation
- `NA` = not applicable for this part/method (blank MWI cell, non-weld raw-material block).
- `NOT FOUND` = required by a governing doc but absent from the package (an evidenced gap).
- Never leave blank. Match the answer-key convention: use `NA` for not-applicable blocks.

## R7 — Final Result
- `Approve` — all MANDATORY blocks Pass/valid. Mandatory = COC, Hardness, Dimension,
  Surface Finish, PLUS every NDT the MWI marks applicable. NA blocks are never mandatory.
- `Reject` — a mandatory block is Fail or an unacceptable mismatch.
- `Check` — unresolved data or unproven PO line.
A raw-material NDT NA (per R2) is NOT a Reject driver.
