# Field → Anchor Map (deterministic extraction contract)

RULE: A field may be set to `NOT FOUND` ONLY after every page of its **owning document**
has been scanned for **every** anchor alias below (English AND Chinese). If any anchor
matches, extract the adjacent value. Never conclude NOT FOUND from a relevance/semantic
search — those miss low-salience footers and sub-pages (this is exactly how the
eye-test date and dimension inspector were missed).

## Low-salience fields that MUST be actively hunted (historical miss list)

| Field | Owning doc | Anchor strings (scan ALL of these) | Notes |
|---|---|---|---|
| Eye Test Examination Date | NDT bundle personnel/vision sub-pages | `检查日期`, `Examination Date`, `Vision Examination Record`, `视力检查`, `下次检验日期`, `Date of Next Examination`, `Near Vision`, `Jaeger` | Often a separate SC-xx form page appended AFTER the NDT report body. Value is the CURRENT exam date, not "next". |
| Inspector qualification | NDT report + attached cert | `ISO 9712`, `ChSNDT`, `Level II`, `级`, `PCN`, `ASNT`, `SNT-TC-1A` | Method+level, e.g. "ISO 9712 UT Level II". |
| Cert Expiry Date | NDT operator cert page | `Date of Expiry`, `有效期`, `失效日期`, `Validity ... till` | |
| Dimension Inspector Name | Dimension / warehouse-out report | `编辑`, `MADE BY`, `检验`, `Inspected By`, `批准`, `Approval` | Usually in the FOOTER of the last page — low salience. |
| Dimension Inspection Date | Dimension report | `日期`, `DATE`, `报告日期` | Footer, paired with MADE BY. |
| Light Band QTY / Status | Optical/Light band report | `光带`, `Optical band detection`, `光带总结`, `Band summary` | |
| Coating Spec / Status | Coating report | `喷涂报告`, `Coating Report`, `规范`, `Standard`, `涂层厚度`, `Coating Thickness`, `5173` | |
| Hardness values/range | Hardness report | `硬度`, `Hardness`, `HRC`, `HBW`, `硬度范围`, `Hardness range` | |
| TN number | COC only | `TN-`, `TN`, `Batch Number`, `批次` | COC only — never from PO/MTC. |
| Surface finish evidence | Drawing FIRST, then MWI | `Ra`, `μin`, `63`, `SODIUM LIGHT BAND`, `LAP`, `SURFACE FINISH`, `表面粗糙度`, `探伤面粗糙度` | Drawing note governs applicability. |

## Owning-document rule (source ownership — never cross-source)
- PO fields → PO only. COC fields → COC only. TN → COC only.
- ERP/Legacy on reports → the report itself; matched against PO, never sourced from drawing/spec/MTC.
- Raw-material NDT stage → material spec / 3024 §11. Finished NDT → MWI + drawing.

## Bilingual anchor discipline
Every Chinese supplier report is bilingual. Always scan BOTH the English and Chinese
label for a field. Missing the Chinese label is the #1 cause of false NOT FOUND.
