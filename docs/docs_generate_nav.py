#!/usr/bin/env python3
import tomllib
import tomli_w
from pathlib import Path
import sys

DOCS_DIR = Path("docs")
STANDARDS_ROOT = DOCS_DIR / "standards"
CONFIG_FILE = Path("zensical.toml")
PLACEHOLDER = "contents_placeholder"
NAV_KEY = "nav"
NAV_STRUCTURE_KEY = "nav_structure"
INDEXES_DIR = "indexes"

def to_title_case(kebab_str: str) -> str:
    """Convert kebab-case to Title Case (e.g., 'test-cat' -> 'Test Cat')"""
    return ' '.join(word.capitalize() for word in kebab_str.split('-'))

def build_tree(root: Path) -> dict:
    """
    Build a tree structure from the standards directory.
    Returns dict with keys:
      - 'standards': list of paths (relative to DOCS_DIR) for standard files at this level
      - 'subdirs': dict of subdirectory name -> tree for that subdir
      - 'has_index': bool if index.md exists at this level
      - 'index_path': relative path to index.md if exists
    """
    tree = {
        'standards': [],
        'subdirs': {},
        'has_index': False,
        'index_path': None
    }

    # Check for index.md at this level
    index_file = root / "index.md"
    if index_file.exists():
        tree['has_index'] = True
        tree['index_path'] = str(index_file.relative_to(DOCS_DIR).as_posix())

    # Scan contents
    for item in root.iterdir():
        if item.is_dir():
            sub_tree = build_tree(item)
            if sub_tree['standards'] or sub_tree['subdirs'] or sub_tree['has_index']:
                tree['subdirs'][item.name] = sub_tree
        elif item.is_file() and item.suffix == '.md':
            if item.name in ['guide.md', 'spec.md', 'template.md']:
                rel_path = str(item.relative_to(DOCS_DIR).as_posix())
                tree['standards'].append(rel_path)

    # If this folder has standards, it's a leaf standard folder, so ignore its subdirs
    if tree['standards']:
        tree['subdirs'] = {}

    tree['standards'] = sorted(set(tree['standards']))
    return tree

def build_nav_section(doc_type: str, tree: dict) -> list:
    """
    Build a navigation section for a specific doc type.
    Returns a list of items (strings or dicts) for this level.
    """
    items = []

    # Add index.md if exists at this level
    if tree['has_index']:
        items.append(tree['index_path'])

    # Process subdirectories
    for subdir_name, sub_tree in sorted(tree['subdirs'].items()):
        # Check if this subdir is a standard (has standard files)
        is_standard = bool(sub_tree['standards'])

        if is_standard:
            # This is a standard folder; add its standard files directly to current level
            # Add index.md if exists at the standard folder level
            if sub_tree['has_index']:
                items.append(sub_tree['index_path'])

            # Add matching standard files
            doc_file_name = f"{doc_type}.md"
            for std_path in sub_tree['standards']:
                if std_path.endswith(f"/{doc_file_name}"):
                    items.append(std_path)
        else:
            # This is a category folder
            title_case_name = to_title_case(subdir_name)
            sub_items = build_nav_section(doc_type, sub_tree)
            if sub_items:
                items.append({title_case_name: sub_items})

    return items

def clean_structure(data):
    def is_index_only(value):
        if not isinstance(value, list):
            return False
        if len(value) != 1:
            return False
        return isinstance(value[0], str) and value[0].endswith("index.md")

    def is_empty_dict(value):
        return isinstance(value, dict) and len(value) == 0

    def clean_recursive(obj):
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                cleaned = clean_recursive(value)
                if cleaned is not None:
                    result[key] = cleaned
            if len(result) == 0:
                return None
            return result
        elif isinstance(obj, list):
            result = []
            for item in obj:
                cleaned = clean_recursive(item)
                if cleaned is not None:
                    result.append(cleaned)

            if len(result) == 0:
                return None
            if len(result) == 1 and isinstance(result[0], str) and result[0].endswith("index.md"):
                return None
            return result
        else:
            return obj

    def deep_clean(obj):
        while True:
            new_obj = clean_recursive(obj)
            if new_obj is None:
                return None
            if isinstance(new_obj, list):
                if len(new_obj) == 1 and isinstance(new_obj[0], str) and new_obj[0].endswith("index.md"):
                    return None
            if new_obj == obj:
                return new_obj
            obj = new_obj

    return deep_clean(data)


def scan_standards():
    """Main function to scan standards and build navigation"""
    if not STANDARDS_ROOT.exists():
        print(f"ERROR: {STANDARDS_ROOT} does not exist", file=sys.stderr)
        return None

    tree = build_tree(STANDARDS_ROOT)

    doc_types = {
        "Guides": "guide",
        "Specifications": "spec",
        "Templates": "template"
    }

    nav_list = []

    for display_name, doc_type in doc_types.items():
        section_items = build_nav_section(doc_type, tree)
        global_index = f"{INDEXES_DIR}/{doc_type}s/index.md"
        section_items = [global_index] + section_items
        nav_list.append({display_name: section_items})

    nav_list = clean_structure(nav_list)
    return nav_list

def update_config(nav_structure):
    """Update zensical.toml: replace placeholder in nav_structure and set nav"""
    if not CONFIG_FILE.exists():
        # Create new config with both nav and nav_structure
        config = {"project": {NAV_KEY: nav_structure, NAV_STRUCTURE_KEY: []}}
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(config, f)
        return

    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)

    if "project" not in config:
        config["project"] = {}

    # Read base nav structure from nav_structure key, fallback to nav
    nav_structure_base = config["project"].get(NAV_STRUCTURE_KEY)
    if nav_structure_base is None:
        # If nav_structure doesn't exist, use current nav as base and save it for future
        nav_structure_base = config["project"].get(NAV_KEY, [])
        config["project"][NAV_STRUCTURE_KEY] = nav_structure_base

    # Replace placeholder in the base structure
    if isinstance(nav_structure_base, list) and PLACEHOLDER in nav_structure_base:
        index = nav_structure_base.index(PLACEHOLDER)
        new_nav = nav_structure_base[:index] + nav_structure + nav_structure_base[index+1:]
        config["project"][NAV_KEY] = new_nav
    else:
        # Placeholder not found: warn and keep nav unchanged (or optionally overwrite with base)
        print(f"WARNING: Placeholder '{PLACEHOLDER}' not found in {NAV_STRUCTURE_KEY}. Replacing {NAV_KEY} with generated tree.", file=sys.stderr)
        # If you want to overwrite nav with the base structure (without placeholder), uncomment:
        config["project"][NAV_KEY] = nav_structure

    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)

def main():
    nav_structure = scan_standards()
    if nav_structure is None:
        sys.exit(1)

    if not nav_structure:
        print("WARNING: No standards found in docs/standards/", file=sys.stderr)
        sys.exit(0)

    update_config(nav_structure)
    print(f"DONE: Updated {CONFIG_FILE} with navigation structure (using {NAV_STRUCTURE_KEY} as base)")

if __name__ == "__main__":
    main()
