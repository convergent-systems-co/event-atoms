#!/usr/bin/env python3
"""Build exports/catalog.json and web/public/exports/catalog.json from validated atoms.

Walks atoms/, streams/, rules/; validates each file against its schema;
assembles a single machine-readable catalog manifest. Exits 1 on validation
failure, 2 on missing dependency.

Usage:
    python scripts/build-exports.py
"""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schemas"
ATOMS_DIR = REPO / "atoms"
COMPOSITIONS_DIR = REPO / "streams"
RULES_DIR = REPO / "rules"
EXPORT_PATH = REPO / "exports" / "catalog.json"
WEB_EXPORT_PATH = REPO / "web" / "public" / "exports" / "catalog.json"
CATALOG_NAME = "event-atoms"
CATALOG_VERSION = "0.1.0"


def load_validator(name: str) -> jsonschema.Draft202012Validator:
    schema_path = SCHEMA_DIR / name
    if not schema_path.exists():
        print(f"error: schema not found: {schema_path}", file=sys.stderr)
        sys.exit(1)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def collect(dir_path: Path, validator: jsonschema.Draft202012Validator, label: str) -> list[dict]:
    if not dir_path.exists():
        return []
    out: list[dict] = []
    for path in sorted(dir_path.rglob("*.json")):
        if path.name == ".gitkeep":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(data))
        if errors:
            print(f"✗ {path.relative_to(REPO)} ({label}):", file=sys.stderr)
            for err in errors:
                loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
                print(f"    {err.message} at {loc}", file=sys.stderr)
            sys.exit(1)
        print(f"  ✓ {path.relative_to(REPO)}")
        out.append(data)
    return out


def main() -> int:
    print(f"Building {CATALOG_NAME} catalog …")

    atom_validator = load_validator("atom-v1.json")
    composition_validator = load_validator("composition-v1.json")
    rule_validator = load_validator("rule-v1.json")

    atoms = collect(ATOMS_DIR, atom_validator, "atom")
    compositions = collect(COMPOSITIONS_DIR, composition_validator, "stream")
    rules = collect(RULES_DIR, rule_validator, "rule")

    catalog = {
        "catalog": CATALOG_NAME,
        "version": CATALOG_VERSION,
        "spec_version": "atoms-spec/v1.1.0",
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "atoms": atoms,
        "compositions": compositions,
        "rules": rules,
    }

    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPORT_PATH.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {EXPORT_PATH.relative_to(REPO)}")

    if WEB_EXPORT_PATH.exists() or WEB_EXPORT_PATH.parent.exists():
        WEB_EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(EXPORT_PATH, WEB_EXPORT_PATH)
        print(f"Copied  {WEB_EXPORT_PATH.relative_to(REPO)}")

    print(f"\n{len(atoms)} atoms  {len(compositions)} streams  {len(rules)} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
