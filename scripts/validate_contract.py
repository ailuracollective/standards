#!/usr/bin/env python3
"""Validate that issue and PR templates match the canonical contract.

This script checks:
1. Issue templates have the correct sections (matching CONTRACT.yml)
2. PR templates have the correct headings (matching CONTRACT.yml)
3. Labels named in templates exist in labels.yml
4. Taxonomy mappings are consistent

Exit code 0 means all validations passed. Exit code 1 means at least one validation failed.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent


def load_yaml(path: Path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_contract():
    return load_yaml(REPO_ROOT / ".github" / "CONTRACT.yml")


def load_issue_templates():
    templates = {}
    template_dir = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"
    for path in template_dir.glob("*.yml"):
        if path.name == "config.yml":
            continue
        template = load_yaml(path)
        templates[path.stem] = template
    return templates


def load_pr_templates():
    templates = {}
    template_dir = REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE"
    for path in template_dir.glob("*.md"):
        template = path.read_text()
        templates[path.stem] = template
    return templates


def load_labels():
    labels = load_yaml(REPO_ROOT / ".github" / "labels.yml")
    return {label["name"] for label in labels}


def validate_issue_templates(contract, templates, labels):
    errors = []
    issue_contract = contract["issue"]
    common_ids = [s["id"] for s in issue_contract["common"]]
    matched_stems = set()

    for type_name, type_contract in issue_contract["types"].items():
        # Find all templates matching this type's title prefix
        matching = [
            (stem, t) for stem, t in templates.items()
            if t.get("title") == type_contract["title_prefix"]
        ]

        if len(matching) == 0:
            errors.append(
                f"Issue type '{type_name}': no template found with title "
                f"'{type_contract['title_prefix']}'"
            )
            continue

        if len(matching) > 1:
            stems = [stem for stem, _ in matching]
            errors.append(
                f"Issue type '{type_name}': multiple templates match title "
                f"'{type_contract['title_prefix']}': {stems}"
            )
            continue

        matched_stems.add(matching[0][0])
        template = matching[0][1]

        # Check labels
        template_labels = set(template.get("labels", []))
        expected_labels = {type_contract["label"], "status/needs-review"}
        if template_labels != expected_labels:
            errors.append(
                f"Issue type '{type_name}': labels {sorted(template_labels)} != expected {sorted(expected_labels)}"
            )

        # Check that all labels exist in labels.yml
        for label in template_labels:
            if label not in labels:
                errors.append(
                    f"Issue type '{type_name}': label '{label}' not found in labels.yml"
                )

        # Collect input fields. `markdown` elements have no id; every other
        # element must carry one, or the template is malformed.
        extra_ids = [s["id"] for s in type_contract.get("extra", [])]
        expected_sections = common_ids + extra_ids
        input_fields = []
        actual_sections = []
        for index, field in enumerate(template.get("body", [])):
            if field.get("type") == "markdown":
                continue
            field_id = field.get("id")
            if not field_id:
                errors.append(
                    f"Issue type '{type_name}': body element {index} of type "
                    f"'{field.get('type')}' is missing a required id"
                )
                continue
            input_fields.append((field, field_id))
            actual_sections.append(field_id)

        # Check that all expected sections are present
        missing = set(expected_sections) - set(actual_sections)
        if missing:
            errors.append(
                f"Issue type '{type_name}': missing sections {sorted(missing)}"
            )

        # Check that there are no extra sections
        unexpected = set(actual_sections) - set(expected_sections)
        if unexpected:
            errors.append(
                f"Issue type '{type_name}': unexpected sections {sorted(unexpected)}"
            )

        # Check that the full sequence matches the contract exactly: the common
        # sections first, then the type-specific sections.
        if actual_sections != expected_sections:
            errors.append(
                f"Issue type '{type_name}': sections {actual_sections} != expected {expected_sections}"
            )

        # Check required/optional validation
        for field, field_id in input_fields:
            is_required = field.get("validations", {}).get("required", False)

            # Find the section in the contract
            section_contract = None
            for section in issue_contract["common"]:
                if section["id"] == field_id:
                    section_contract = section
                    break
            if section_contract is None:
                for section in type_contract.get("extra", []):
                    if section["id"] == field_id:
                        section_contract = section
                        break

            if section_contract:
                expected_required = section_contract["required"]
                if is_required != expected_required:
                    errors.append(
                        f"Issue type '{type_name}' field '{field_id}': required={is_required} != expected {expected_required}"
                    )

    # Check for templates that don't match any contract type
    unmatched = set(templates.keys()) - matched_stems
    if unmatched:
        errors.append(
            f"Unmatched issue templates (no contract type): {sorted(unmatched)}"
        )

    return errors


def validate_pr_templates(contract, templates):
    errors = []
    pr_contract = contract["pr"]
    common_sections = pr_contract["common"]
    common_labels = [s["label"] for s in common_sections]
    required_labels = [s["label"] for s in common_sections if s["required"]]

    for type_name, type_contract in pr_contract["types"].items():
        template = templates.get(type_name)
        if template is None:
            errors.append(f"PR type '{type_name}': no template found")
            continue

        # Check headings
        extra_labels = [s["label"] for s in type_contract.get("extra", [])]

        actual_headings = []
        for line in template.split("\n"):
            if line.startswith("## "):
                heading = line[3:].strip()
                # Strip "(required)" suffix for comparison
                heading = re.sub(r"\s*\(required\)\s*$", "", heading)
                actual_headings.append(heading)

        # Check that all required headings are present
        missing = set(required_labels) - set(actual_headings)
        if missing:
            errors.append(
                f"PR type '{type_name}': missing required headings {sorted(missing)}"
            )

        # Check that all headings are in the contract
        all_expected = set(common_labels + extra_labels)
        extra = set(actual_headings) - all_expected
        if extra:
            errors.append(
                f"PR type '{type_name}': unexpected headings {sorted(extra)}"
            )

        # Check that required common headings appear in the correct relative order
        required_in_template = [h for h in actual_headings if h in required_labels]
        if required_in_template != required_labels:
            errors.append(
                f"PR type '{type_name}': required headings {required_in_template} != expected {required_labels}"
            )

        # Check that type-specific headings appear in the correct relative order
        extra_in_template = [h for h in actual_headings if h in extra_labels]
        if extra_in_template != extra_labels:
            errors.append(
                f"PR type '{type_name}': type-specific headings {extra_in_template} != expected {extra_labels}"
            )

    return errors


def validate_taxonomy(contract, templates, labels):
    errors = []
    taxonomy = contract.get("taxonomy", {})
    issue_contract = contract.get("issue", {})
    pr_contract = contract.get("pr", {})

    # Check that all labels in taxonomy mappings exist in labels.yml
    pr_title_to_label = taxonomy.get("pr_title_to_label", {})
    for pr_type, label in pr_title_to_label.items():
        if label is not None and label not in labels:
            errors.append(
                f"Taxonomy: label '{label}' for PR type '{pr_type}' not found in labels.yml"
            )

    # Check that pr_title_to_label covers all PR types in the contract
    pr_types_in_contract = set(pr_contract.get("types", {}).keys())
    pr_types_in_mapping = set(pr_title_to_label.keys())
    missing_pr_types = pr_types_in_contract - pr_types_in_mapping
    if missing_pr_types:
        errors.append(
            f"Taxonomy: pr_title_to_label missing PR types: {sorted(missing_pr_types)}"
        )

    # Check that issue_to_pr_title covers all issue types in the contract
    issue_to_pr_title = taxonomy.get("issue_to_pr_title", {})
    issue_types_in_contract = set(issue_contract.get("types", {}).keys())
    issue_types_in_mapping = set(issue_to_pr_title.keys())
    missing_issue_types = issue_types_in_contract - issue_types_in_mapping
    if missing_issue_types:
        errors.append(
            f"Taxonomy: issue_to_pr_title missing issue types: {sorted(missing_issue_types)}"
        )

    # Check that issue_to_pr_title values are valid PR types or None
    for issue_type, pr_type in issue_to_pr_title.items():
        if pr_type is not None and pr_type not in pr_types_in_contract:
            errors.append(
                f"Taxonomy: issue_to_pr_title['{issue_type}'] = '{pr_type}' "
                f"is not a valid PR type"
            )

    # Check that pr_title_to_branch covers all PR types
    pr_title_to_branch = taxonomy.get("pr_title_to_branch", {})
    missing_branch_types = pr_types_in_contract - set(pr_title_to_branch.keys())
    if missing_branch_types:
        errors.append(
            f"Taxonomy: pr_title_to_branch missing PR types: {sorted(missing_branch_types)}"
        )

    return errors


def main():
    contract = load_contract()
    issue_templates = load_issue_templates()
    pr_templates = load_pr_templates()
    labels = load_labels()

    errors = []
    errors.extend(validate_issue_templates(contract, issue_templates, labels))
    errors.extend(validate_pr_templates(contract, pr_templates))
    errors.extend(validate_taxonomy(contract, issue_templates, labels))

    if errors:
        print("Contract validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Contract validation passed.")


if __name__ == "__main__":
    main()
