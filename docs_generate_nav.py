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

    return nav_list

def update_config(nav_structure):
    """Update zensical.toml: replace placeholder or set nav key"""
    if not CONFIG_FILE.exists():
        config = {"project": {NAV_KEY: nav_structure}}
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(config, f)
        return

    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)

    if "project" not in config:
        config["project"] = {}

    if NAV_KEY in config["project"]:
        existing = config["project"][NAV_KEY]
        if isinstance(existing, list) and PLACEHOLDER in existing:
            index = existing.index(PLACEHOLDER)
            new_nav = existing[:index] + nav_structure + existing[index+1:]
            config["project"][NAV_KEY] = new_nav
        else:
            config["project"][NAV_KEY] = nav_structure
    else:
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
    print(f"DONE: Updated {CONFIG_FILE} with navigation structure")

if __name__ == "__main__":
    main()
