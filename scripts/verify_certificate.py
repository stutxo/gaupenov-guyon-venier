#!/usr/bin/env python3
"""Reproduce the announcement and auxiliary textual certificates with Python."""

import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, label: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {label}")
    print(f"PASS: {label}")


def read_definition(source: str, name: str) -> str:
    match = re.search(rf'def {re.escape(name)}\s*:\s*String\s*:=\s*"([^"\n]*)"', source)
    if match is None:
        raise SystemExit(f"String definition not found: {name}")
    return match.group(1)


def read_integer(source: str, name: str) -> int:
    match = re.search(rf'def {re.escape(name)}\s*:\s*(?:Int|Nat)\s*:=\s*([0-9]+)', source)
    if match is None:
        raise SystemExit(f"Integer definition not found: {name}")
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reveal", action="store_true", help="display the decoded certificates")
    args = parser.parse_args()
    texts = (ROOT / "GaupenovGuyonVenier/TextCertificates.lean").read_text()
    definitions = (ROOT / "GaupenovGuyonVenier/Definitions.lean").read_text()
    reference = (ROOT / "GaupenovGuyonVenier/Certificate.lean").read_text()
    first = read_definition(texts, "retentionText")
    second = read_definition(texts, "stabilityText")
    first_code = read_integer(texts, "retentionCode")
    second_code = read_integer(texts, "stabilityCode")
    witness = read_integer(definitions, "witnessA")
    require(int.from_bytes(hashlib.sha256(first.encode("ascii")).digest(), "big") == witness,
            "announced SHA-256 integer")
    require(first_code.to_bytes(23, "big").decode("ascii") == first,
            "23-byte retention certificate")
    require(second_code.to_bytes(24, "big").decode("ascii") == second,
            "24-byte stability certificate")
    normalize = lambda value: Counter(c.lower() for c in value if c.isalpha())
    require(normalize("GaupenovGuyonVenier") == normalize(first), "title anagram certificate")
    if args.reveal:
        print()
        print(first)
        print(second)
        print(read_definition(reference, "referenceURL"))


if __name__ == "__main__":
    main()
