#!/usr/bin/env python3
"""Report local readiness for the ACE2 evolutionary genomics pipeline."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def version(cmd: str) -> str:
    path = shutil.which(cmd)
    if not path:
        return "MISSING"
    probes = ([cmd, "--version"], [cmd, "-version"], [cmd, "-h"])
    for probe in probes:
        try:
            out = subprocess.run(probe, check=False, capture_output=True, text=True, timeout=5)
        except Exception:
            continue
        text = (out.stdout or out.stderr).strip().splitlines()
        if text:
            return f"{path} | {text[0][:120]}"
    return path


def main() -> int:
    print(f"Project: {ROOT}")
    print(f"Python: {sys.executable}")
    for cmd in [
        "datasets",
        "esearch",
        "efetch",
        "blastp",
        "mafft",
        "muscle",
        "iqtree2",
        "iqtree",
        "hyphy",
        "codeml",
        "Rscript",
        "make",
    ]:
        print(f"{cmd}: {version(cmd)}")

    for rel in [
        "config/genes.tsv",
        "config/target_species.tsv",
        "config/residue_annotations.tsv",
        "config/trait_schema.tsv",
    ]:
        print(f"{rel}: {'OK' if (ROOT / rel).exists() else 'MISSING'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
