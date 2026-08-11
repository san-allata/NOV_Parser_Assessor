# Output Schema — the authoritative 149-column A→ES layout (MANDATORY)

The workbook row MUST follow this exact column order and these exact header labels.
Row 1 = Header Group. Row 2 = Sub-header. Row 3 = the data value. Never reorder,
rename, insert, or drop a column. Dates stored as TEXT. No blank cells (use value / NA /
NOT FOUND). This schema is the single source of truth — it supersedes any reconstructed
layout.

| Col | Header Group | Sub-header | Owning source |
|-----|--------------|-----------|---------------|
| A  | Case | Case label | derived: `<PO no.>-<ERP>-<date>-<supplier short>` |
| B  | MWI | MWI | MWI |
| C  | PO | Supplier Name | PO |
| D  | PO | PO line no. | PO |
| E  | PO | PO no. | PO |
| F  | PO | ERP ID | PO |
| G  | PO | Legacy ID | PO |
| H  | PO | QTY | PO |
| I  | PO | NCL | PO |
| J  | COC | PO line no. | COC |
| K  | COC | PO no. | COC |
| L  | COC | ERP ID | COC |
| M  | COC | Legacy ID | COC |
| N  | COC | QTY | COC |
| O  | COC | NCL Level | COC |
| P  | COC | TN number | COC |
| Q  | COC | Serial Number | COC |
| R  | COC | Status | derived Pass/Fail |
| S  | 3.1 MTC | Status | derived Yes/No |
| T  | Balloon Drawing | Status | derived Yes/No |
| U  | Dimension Report | PO no. | Dimension Report |
| V  | Dimension Report | ERP ID | Dimension Report |
| W  | Dimension Report | Legacy ID | Dimension Report |
| X  | Dimension Report | Sampling Inspection QTY | Dimension Report |
| Y  | Dimension Report | Inspector Name | Dimension Report |
| Z  | Dimension Report | Inspection Date | Dimension Report |
| AA | Dimension Report | Status | derived Pass/Fail |
| AB | Surface Finish | Status | derived Yes/No |
| AC | Hardness Report | PO no. | Hardness Report |
| AD | Hardness Report | ERP ID | Hardness Report |
| AE | Hardness Report | Legacy ID | Hardness Report |
| AF | Hardness Report | QTY | Hardness Report |

## Repeating 11-field NDT block layout
The following blocks each use the SAME 11 sub-headers, in this exact order:
`PO no. | ERP ID | Legacy ID | QTY | Test Date | Inspector Name | Testing Spec |
Inspector qualification | Expiry Date | Eye Test Examination Date | Status`

| Cols | Block (Header Group) |
|------|----------------------|
| AG–AQ | MPI Report (Material) |
| AR–BB | LPI Report (Material) |
| BC–BM | UT Report (Material) |
| BN–BX | RT Report (Material) |
| BY–CI | MPI Report (Finished Product) |
| CJ–CT | LPI Report (Finished Product) |
| CU–DE | UT Report (Finished Product) |
| DF–DP | RT Report (Finished Product) |
| DQ–EA | Ultrasonic Gauge Thickness Report |

## Tail blocks
| Col | Header Group | Sub-header | Notes |
|-----|--------------|-----------|-------|
| EB | Coating Report | PO no. | |
| EC | Coating Report | ERP ID | |
| ED | Coating Report | Legacy ID | |
| EE | Coating Report | QTY | |
| EF | Coating Report | Spec | |
| EG | Coating Report | Status | Pass/Fail/NA |
| EH | Light Band Report | PO no. | |
| EI | Light Band Report | ERP ID | |
| EJ | Light Band Report | Legacy ID | |
| EK | Light Band Report | QTY | |
| EL | Light Band Report | Status | Pass/Fail/NA |
| EM | PWHT Report | Status | Yes/No only |
| EN | Concession | Concession no. | |
| EO | Concession | Status | Yes/No only |
| EP | NCR | NCR no. | |
| EQ | NCR | Status | Yes/No only |
| ER | Remarks | Remarks | concise reason for Fail/Check |
| ES | Final Result | Final Result | Approve / Reject / Check |

## Save-lock (must pass before writing the workbook)
1. Exactly 149 columns; last column resolves to ES.
2. No blank cells anywhere.
3. Every date cell stored as TEXT (`@` format) — never an Excel serial (e.g. 45903).
4. PWHT / Concession / NCR Status cells contain ONLY `Yes` or `No`.
5. NDT block Status cells are one of: `Pass` / `Fail` / `Check` / `NA`.
6. Run `scripts/completeness_gate.py` and pass before saving.

## Reference generator
`scripts/build_row.py` builds a schema-correct, styled workbook from a flat dict of
values so the column order can never drift by hand.

