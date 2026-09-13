#!/usr/bin/env python3
"""Generate protocol.h and Protocol.kt from PROTOCOL.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "PROTOCOL.md"
C_HEADER = ROOT / "protocol.h"
KOTLIN_HEADER = ROOT / "Protocol.kt"


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    return all(re.fullmatch(r":?-+:?", cell) for cell in cells(line))


def tables(markdown: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = markdown.splitlines()
    result = []
    index = 0
    while index + 1 < len(lines):
        if not lines[index].lstrip().startswith("|") or not is_separator(lines[index + 1]):
            index += 1
            continue

        header = cells(lines[index])
        rows = []
        index += 2
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            row = cells(lines[index])
            if len(row) != len(header):
                raise ValueError(f"table row has the wrong number of columns: {lines[index]}")
            rows.append(row)
            index += 1
        result.append((header, rows))
    return result


def find_tables(all_tables, columns: list[str]):
    matches = [rows for header, rows in all_tables if header == columns]
    if not matches:
        raise ValueError(f"could not find table with columns: {columns}")
    return matches


def find_table(all_tables, columns: list[str]):
    matches = find_tables(all_tables, columns)
    if len(matches) != 1:
        raise ValueError(f"expected one table with columns: {columns}")
    return matches[0]


def parse_spec(markdown: str):
    version_match = re.search(r"\*\*Draft of Version (\d+)\*\*", markdown)
    if not version_match:
        raise ValueError("could not find '**Draft of Version N**' in PROTOCOL.md")
    version = int(version_match.group(1))

    all_tables = tables(markdown)
    key_rows = []
    for rows in find_tables(all_tables, ["Key", "Name", "Type", "Description"]):
        key_rows.extend(rows)

    keys = []
    names = set()
    values = set()
    for row in key_rows:
        if not re.fullmatch(r"\d+", row[0]):
            continue
        key = int(row[0])
        name = row[1]
        value_type = row[2]
        if not name:
            continue
        if name in names or key in values:
            raise ValueError(f"duplicate message key or name: {key}, {name}")
        if not name.startswith("KEY_"):
            raise ValueError(f"message name is not a KEY_ identifier: {name}")
        names.add(name)
        values.add(key)
        keys.append((key, name, value_type))

    capability_rows = find_table(all_tables, ["Name", "Mask", "Description"])
    capabilities = []
    capability_names = set()
    capability_masks = set()
    for row in capability_rows:
        name, mask_text = row[0], row[1].strip("`")
        if not name:
            continue
        if not name.startswith("CAP_"):
            raise ValueError(f"capability name is not a CAP_ identifier: {name}")
        try:
            mask = int(mask_text, 16)
        except ValueError as error:
            raise ValueError(f"invalid capability mask: {row[1]}") from error
        if mask <= 0 or mask & (mask - 1) or mask in capability_masks:
            raise ValueError(f"capability mask is not unique and one-bit: {row[1]}")
        if name in capability_names:
            raise ValueError(f"duplicate capability name: {name}")
        capability_names.add(name)
        capability_masks.add(mask)
        capabilities.append((name, mask))

    trend_rows = find_table(all_tables, ["Name", "Index", "Description"])
    trends = []
    trend_names = set()
    trend_indices = set()
    for row in trend_rows:
        name = row[0]
        if not name:
            continue
        if not name.startswith("TREND_"):
            raise ValueError(f"trend name is not a TREND_ identifier: {name}")
        index = int(row[1])
        if name in trend_names or index in trend_indices:
            raise ValueError(f"duplicate trend name or index: {name}, {index}")
        trend_names.add(name)
        trend_indices.add(index)
        trends.append((name, index))

    return version, sorted(keys), capabilities, trends


def generate_c(version, keys, capabilities, trends) -> str:
    lines = [
        "// Pebble Glucose Protocol",
        "//",
        "// Generated from PROTOCOL.md. Do not edit directly.",
        "",
        "#pragma once",
        "",
        f"#define PROTOCOL_VERSION {version}",
        "",
        "// Message keys: Watchface -> sender (capability announcement)",
    ]
    lines += [f"#define {name} {key}" for key, name, _ in keys if key < 10]
    lines += [
        "// Keys 3-9 reserved",
        "",
        "// Message keys: Sender -> watchface (data)",
    ]
    lines += [f"#define {name} {key}" for key, name, _ in keys if 10 <= key < 30]
    lines += [
        "// Keys 19-29 reserved",
        "",
        "// Message keys: Sender -> watchface (raw graph)",
    ]
    lines += [f"#define {name} {key}" for key, name, _ in keys if 30 <= key < 40]
    lines += [
        "// Keys 33-39 reserved",
        "",
        "// Keys 40-49 reserved for bitmap graph",
        "",
        "// Capability bits",
    ]
    lines += [f"#define {name} 0x{mask:02x}" for name, mask in capabilities]
    lines += ["", "// Trend arrow indices"]
    lines += [f"#define {name} {index}" for name, index in trends]
    return "\n".join(lines) + "\n"


def generate_kotlin(version, keys, capabilities, trends) -> str:
    lines = [
        "// Pebble Glucose Protocol",
        "//",
        "// Generated from PROTOCOL.md. Do not edit directly.",
        "",
        "object Protocol {",
        f"    const val PROTOCOL_VERSION = {version}",
        "",
        "    // Keys are UInt because that is what PebbleKit Android 2 dictionaries take.",
        "",
        "    // Message keys: Watchface -> sender (capability announcement)",
    ]
    lines += [f"    const val {name}: UInt = {key}u" for key, name, _ in keys if key < 10]
    lines += [
        "    // Keys 3-9 reserved",
        "",
        "    // Message keys: Sender -> watchface (data)",
    ]
    lines += [f"    const val {name}: UInt = {key}u" for key, name, _ in keys if 10 <= key < 30]
    lines += [
        "    // Keys 19-29 reserved",
        "",
        "    // Message keys: Sender -> watchface (raw graph)",
    ]
    lines += [f"    const val {name}: UInt = {key}u" for key, name, _ in keys if 30 <= key < 40]
    lines += [
        "    // Keys 33-39 reserved",
        "",
        "    // Keys 40-49 reserved for bitmap graph",
        "",
        "    // Capability bits",
    ]
    lines += [f"    const val {name} = 0x{mask:02x}" for name, mask in capabilities]
    lines += ["", "    // Trend arrow indices"]
    lines += [f"    const val {name} = {index}" for name, index in trends]
    lines += ["}"]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    args = parser.parse_args()

    try:
        version, keys, capabilities, trends = parse_spec(SPEC.read_text())
        generated = {
            C_HEADER: generate_c(version, keys, capabilities, trends),
            KOTLIN_HEADER: generate_kotlin(version, keys, capabilities, trends),
        }
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, content in generated.items() if path.read_text() != content]
        if stale:
            print("generated files are out of date: " + ", ".join(stale), file=sys.stderr)
            return 1
        return 0

    for path, content in generated.items():
        path.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
