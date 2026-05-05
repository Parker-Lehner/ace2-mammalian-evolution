#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE5 = ROOT / "phase5_hyphy_ecological_validation"
FOREGROUNDS = ["cetacean", "deep_diving", "aquatic", "marine"]

def nested(data, keys):
    cur = data
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur

def first(data, paths):
    for path in paths:
        value = nested(data, path)
        if value is not None:
            return value
    return None

def bh(rows):
    vals = [(i, float(r["p_value"])) for i, r in enumerate(rows) if r["p_value"] not in ("", "NA")]
    m = len(vals)
    passed = set()
    for rank, (idx, p) in enumerate(sorted(vals, key=lambda x: x[1]), start=1):
        if p <= (rank / m) * 0.10:
            passed.add(idx)
    return passed

def parse_busted(data):
    p = first(data, [
        ["test results", "p-value"],
        ["test results", "p"],
        ["test results", "LRT"],
    ])
    lrt = first(data, [["test results", "LRT"]])
    return lrt, p

def attr_value(attrs, keys):
    for key in keys:
        if key in attrs and attrs[key] is not None:
            return attrs[key]
    return None

def parse_absrel(data):
    tested = first(data, [["test results", "tested"]])
    positive = first(data, [["test results", "positive test results"]])
    pvals = []
    branch_attrs = data.get("branch attributes", {})
    for attrs_by_tree in branch_attrs.values() if isinstance(branch_attrs, dict) else []:
        if not isinstance(attrs_by_tree, dict):
            continue
        for branch, attrs in attrs_by_tree.items():
            if not isinstance(attrs, dict):
                continue
            p = attr_value(attrs, ["Corrected P-value", "P-value", "p"])
            if p is not None:
                try:
                    pvals.append(float(p))
                except Exception:
                    pass
    min_p = min(pvals) if pvals else None
    return tested, positive, min_p

def absrel_branch_rows(fg, data):
    rows = []
    branch_attrs = data.get("branch attributes", {})
    for attrs_by_tree in branch_attrs.values() if isinstance(branch_attrs, dict) else []:
        if not isinstance(attrs_by_tree, dict):
            continue
        for branch, attrs in attrs_by_tree.items():
            if not isinstance(attrs, dict):
                continue
            corrected = attr_value(attrs, ["Corrected P-value", "P-value", "p"])
            uncorrected = attr_value(attrs, ["Uncorrected P-value"])
            lrt = attr_value(attrs, ["LRT"])
            if corrected is None and uncorrected is None and lrt is None:
                continue
            try:
                corrected_f = float(corrected) if corrected is not None else None
            except Exception:
                corrected_f = None
            rows.append({
                "foreground_group": fg,
                "branch": branch,
                "corrected_p_value": "" if corrected is None else corrected,
                "uncorrected_p_value": "" if uncorrected is None else uncorrected,
                "lrt": "" if lrt is None else lrt,
                "significant_corrected_0_05": str(corrected_f is not None and corrected_f < 0.05).lower(),
            })
    return rows

def main():
    rows = []
    branch_rows = []
    for fg in FOREGROUNDS:
        for method in ["busted", "absrel"]:
            path = PHASE5 / "hyphy_results" / f"{fg}_{method}.json"
            if not path.exists() or path.stat().st_size == 0:
                rows.append({"foreground_group": fg, "method": method, "status": "missing", "lrt_or_tested": "", "p_value": "", "positive_branches": "", "significant_nominal_0_05": "false", "significant_bh_fdr_0_10": "false", "warnings": "missing JSON"})
                continue
            try:
                data = json.loads(path.read_text())
            except Exception as exc:
                rows.append({"foreground_group": fg, "method": method, "status": "parse_error", "lrt_or_tested": "", "p_value": "", "positive_branches": "", "significant_nominal_0_05": "false", "significant_bh_fdr_0_10": "false", "warnings": str(exc)})
                continue
            if method == "busted":
                lrt, p = parse_busted(data)
                pstr = "" if p is None else str(p)
                rows.append({"foreground_group": fg, "method": method, "status": "completed", "lrt_or_tested": "" if lrt is None else str(lrt), "p_value": pstr, "positive_branches": "", "significant_nominal_0_05": str(p is not None and float(p) < 0.05).lower(), "significant_bh_fdr_0_10": "false", "warnings": ""})
            else:
                tested, positive, min_p = parse_absrel(data)
                branch_rows.extend(absrel_branch_rows(fg, data))
                pstr = "" if min_p is None else str(min_p)
                rows.append({"foreground_group": fg, "method": method, "status": "completed", "lrt_or_tested": "" if tested is None else str(tested), "p_value": pstr, "positive_branches": "" if positive is None else str(positive), "significant_nominal_0_05": str(min_p is not None and float(min_p) < 0.05).lower(), "significant_bh_fdr_0_10": "false", "warnings": "aBSREL p-value is minimum branch corrected p-value when available"})
    passed = bh(rows)
    for idx in passed:
        rows[idx]["significant_bh_fdr_0_10"] = "true"
    out = PHASE5 / "hyphy_results/phase5_hyphy_summary.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["foreground_group","method","status","lrt_or_tested","p_value","positive_branches","significant_nominal_0_05","significant_bh_fdr_0_10","warnings"]
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    branch_out = PHASE5 / "hyphy_results/phase5_absrel_branch_results.tsv"
    branch_fields = ["foreground_group","branch","corrected_p_value","uncorrected_p_value","lrt","significant_corrected_0_05"]
    with branch_out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=branch_fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(sorted(branch_rows, key=lambda r: (r["foreground_group"], float(r["corrected_p_value"]) if r["corrected_p_value"] not in ("", None) else 999, r["branch"])))
    print(f"Wrote {out}")
    print(f"Wrote {branch_out}")
if __name__ == "__main__":
    main()
