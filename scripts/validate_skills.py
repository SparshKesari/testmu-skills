#!/usr/bin/env python3
"""Validate all skills in the TestMu Skills repository."""

import os
import re
import sys
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'evals', 'shared', '.git', 'scripts', 'docs', '__pycache__'}
MAX_SKILL_LINES = 500

VALID_CATEGORIES = {
    'accessibility', 'api-testing', 'bdd-testing', 'cloud-testing',
    'devops', 'e2e-testing', 'mobile-testing', 'performance-testing',
    'security-testing', 'unit-testing', 'visual-testing',
}

errors = []
warnings = []
skills_found = 0


def validate_frontmatter(skill_dir, content):
    """Validate YAML frontmatter structure."""
    if not content.startswith('---\n'):
        errors.append(f"{skill_dir}: Missing opening --- in frontmatter")
        return False

    fm_end = content.find('\n---\n', 3)
    if fm_end == -1:
        fm_end = content.find('\n---', 3)
    if fm_end == -1:
        errors.append(f"{skill_dir}: Missing closing --- in frontmatter")
        return False

    fm = content[4:fm_end]

    if not re.search(r'^name:', fm, re.MULTILINE):
        errors.append(f"{skill_dir}: Missing 'name' in frontmatter")
    if not re.search(r'^description:', fm, re.MULTILINE):
        errors.append(f"{skill_dir}: Missing 'description' in frontmatter")
    if not re.search(r'^languages:', fm, re.MULTILINE):
        warnings.append(f"{skill_dir}: Missing 'languages' in frontmatter")
    if not re.search(r'^category:', fm, re.MULTILINE):
        warnings.append(f"{skill_dir}: Missing 'category' in frontmatter")
    else:
        cat = re.search(r'^category:\s*(.+)', fm, re.MULTILINE)
        if cat and cat.group(1).strip() not in VALID_CATEGORIES:
            warnings.append(f"{skill_dir}: Unknown category '{cat.group(1).strip()}'")

    return True


def validate_skill(skill_dir):
    """Validate a single skill directory."""
    global skills_found
    skill_path = os.path.join(REPO_ROOT, skill_dir)
    skill_md = os.path.join(skill_path, 'SKILL.md')

    if not os.path.exists(skill_md):
        errors.append(f"{skill_dir}: Missing SKILL.md")
        return

    skills_found += 1

    with open(skill_md) as f:
        content = f.read()

    # Check line count
    lines = len(content.split('\n'))
    if lines > MAX_SKILL_LINES:
        errors.append(f"{skill_dir}: SKILL.md is {lines} lines (max {MAX_SKILL_LINES})")

    # Validate frontmatter
    validate_frontmatter(skill_dir, content)

    # Check for reference directory
    ref_dir = os.path.join(skill_path, 'reference')
    if not os.path.isdir(ref_dir):
        warnings.append(f"{skill_dir}: No reference/ directory")
    else:
        playbook = os.path.join(ref_dir, 'playbook.md')
        if not os.path.exists(playbook):
            warnings.append(f"{skill_dir}: No reference/playbook.md")

    # Check that SKILL.md references its reference files
    if 'reference/' not in content and 'playbook.md' not in content:
        warnings.append(f"{skill_dir}: SKILL.md doesn't reference playbook.md")


def main():
    print("=" * 60)
    print("TestMu Skills Validation")
    print("=" * 60)

    for item in sorted(os.listdir(REPO_ROOT)):
        item_path = os.path.join(REPO_ROOT, item)
        if os.path.isdir(item_path) and item not in SKIP_DIRS and not item.startswith('.'):
            if os.path.exists(os.path.join(item_path, 'SKILL.md')):
                validate_skill(item)

    # Print results
    print(f"\nSkills found: {skills_found}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\n❌ ERRORS:")
        for e in errors:
            print(f"  {e}")

    if warnings:
        print("\n⚠️  WARNINGS:")
        for w in warnings:
            print(f"  {w}")

    if not errors:
        print("\n✅ All skills pass validation!")
        return 0
    else:
        print("\n❌ Validation failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
