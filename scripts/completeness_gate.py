#!/usr/bin/env python3
"""Completeness gate for NOV MRB rows. Run BEFORE emitting a row.

Usage: build `row` (dict field->value) and `scan_log` (dict field->list_of_pages_scanned),
then call validate(row, scan_log, context). Raises GateError on any violation.
This makes the two historical failure classes impossible to ship silently:
  (1) missed value -> NOT FOUND without an evidenced scan is rejected
  (2) wrong status -> forbidden raw-material-NDT Fail default is rejected
"""

class GateError(Exception):
    pass

MATERIAL_NDT = ["MPI Report (Material)", "LPI Report (Material)",
                "UT Report (Material)", "RT Report (Material)"]
LOW_SALIENCE = [  # fields historically missed; must have a scan-log entry if NOT FOUND
    "Eye Test Examination Date", "Inspector qualification", "Cert Expiry Date",
    "Dimension Inspector Name", "Dimension Inspection Date",
    "Light Band QTY", "Coating Spec",
]

def validate(row: dict, scan_log: dict, context: dict) -> None:
    """context keys used:
        finished_pass_methods: set of methods with a passing FINISHED report, e.g. {'UT','MPI','PT'}
        part_is_weld: bool
    """
    errors = []

    # 1) No blank cells anywhere.
    for field, val in row.items():
        if val is None or str(val).strip() == "":
            errors.append(f"BLANK cell: '{field}' (use value / NA / NOT FOUND)")

    # 2) NOT FOUND must be evidenced by a logged scan of the owning doc.
    for field, val in row.items():
        if str(val).strip().upper() == "NOT FOUND":
            pages = scan_log.get(field)
            if not pages:
                errors.append(
                    f"UNEVIDENCED NOT FOUND: '{field}' has no scan_log entry. "
                    f"Scan the owning document's pages for all anchors before NOT FOUND.")

    # 3) Forbidden default: raw-material NDT = Fail when finished-stage of same method passed.
    method_of = {"MPI Report (Material)": "MPI", "LPI Report (Material)": "PT",
                 "UT Report (Material)": "UT", "RT Report (Material)": "RT"}
    for block in MATERIAL_NDT:
        status = str(row.get(f"{block} :: Status", row.get(block, ""))).strip().lower()
        m = method_of[block]
        if status == "fail" and m in context.get("finished_pass_methods", set()) \
           and not context.get("part_is_weld", False):
            errors.append(
                f"FORBIDDEN Fail: {block} cannot be Fail — a passing finished {m} "
                f"report exists and part is non-weld (rule R2 -> use NA).")

    # 4) Finished NDT Check caused only by missing eye-test w/o a logged re-scan.
    for method, block in [("MPI", "MPI Report (Finished Product)"),
                          ("PT", "LPI Report (Finished Product)"),
                          ("UT", "UT Report (Finished Product)")]:
        status = str(row.get(f"{block} :: Status", "")).strip().lower()
        eye = str(row.get(f"{block} :: Eye Test Examination Date", "")).strip().upper()
        if status == "check" and eye == "NOT FOUND" \
           and not scan_log.get(f"{block} :: Eye Test Examination Date"):
            errors.append(
                f"UNVERIFIED Check: {block} downgraded for missing eye-test without a "
                f"logged re-scan of the vision sub-pages (rule R3).")

    if errors:
        raise GateError("Completeness gate FAILED:\n  - " + "\n  - ".join(errors))
    return None


if __name__ == "__main__":
    # Smoke test: the exact bug that shipped originally must now be caught.
    bad = {"UT Report (Material) :: Status": "Fail",
           "UT Report (Finished Product) :: Eye Test Examination Date": "NOT FOUND",
           "UT Report (Finished Product) :: Status": "Check"}
    try:
        validate(bad, {}, {"finished_pass_methods": {"UT"}, "part_is_weld": False})
        print("ERROR: gate should have failed")
    except GateError as e:
        print("OK - gate correctly blocked the original bug:\n", e)
