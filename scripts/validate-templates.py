#!/usr/bin/env python3
"""
Template Validation Script for Harness Agent Templates

Validates templates against the rules defined in claude.md:
- metadata.json: Valid JSON, required fields, naming conventions
- pipeline.yaml: Valid YAML, required structure, input validation
- wiki.MD: Optional, checks required sections if present
- Cross-file consistency checks

Exit codes:
  0 - All validations passed
  1 - Validation errors found
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# Try to import yaml, provide helpful error if not available
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


class ValidationResult:
    """Tracks validation results for a template."""

    def __init__(self, template_name: str):
        self.template_name = template_name
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_pass(self, message: str) -> None:
        self.passes.append(message)

    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_report(self) -> None:
        print(f"\n## Template: {self.template_name}")
        print("-" * 50)

        for msg in self.passes:
            print(f"  ✅ {msg}")
        for msg in self.warnings:
            print(f"  ⚠️  {msg}")
        for msg in self.errors:
            print(f"  ❌ {msg}")

        print(f"\n  Summary: {len(self.errors)} errors, {len(self.warnings)} warnings")
        if self.is_valid():
            print("  Status: PASSED")
        else:
            print("  Status: FAILED")


def validate_metadata_json(template_dir: Path, result: ValidationResult) -> dict | None:
    """Validate metadata.json file."""
    metadata_path = template_dir / "metadata.json"

    if not metadata_path.exists():
        result.add_error("metadata.json: File not found (required)")
        return None

    # Check JSON syntax
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        result.add_pass("metadata.json: Valid JSON syntax")
    except json.JSONDecodeError as e:
        result.add_error(f"metadata.json: Invalid JSON syntax - {e}")
        return None

    # Check required fields
    required_fields = ['name', 'description', 'version']
    for field in required_fields:
        if field not in metadata:
            result.add_error(f"metadata.json: Missing required field '{field}'")

    # Validate 'name' field
    if 'name' in metadata:
        name = metadata['name']

        # Must be lowercase with spaces only (alphanumeric)
        if not re.match(r'^[a-z0-9 ]+$', name):
            result.add_error(
                f"metadata.json: 'name' must be lowercase alphanumeric with spaces only. "
                f"Got: '{name}'"
            )
        else:
            result.add_pass("metadata.json: 'name' follows naming conventions")

        # Check if name matches directory name (spaces instead of hyphens)
        dir_name = template_dir.name
        expected_name = dir_name.replace('-', ' ')
        if name != expected_name:
            result.add_warning(
                f"metadata.json: 'name' should match directory name. "
                f"Expected: '{expected_name}', Got: '{name}'"
            )

    # Validate 'description' field
    if 'description' in metadata:
        desc = metadata['description']

        # Should end with proper punctuation
        if not desc.rstrip().endswith(('.', '!', '?')):
            result.add_warning("metadata.json: 'description' should end with punctuation")
        else:
            result.add_pass("metadata.json: 'description' has proper punctuation")

    # Validate 'version' field (semver)
    if 'version' in metadata:
        version = metadata['version']

        # Must match semver pattern: MAJOR.MINOR.PATCH
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            result.add_error(
                f"metadata.json: 'version' must follow semver (MAJOR.MINOR.PATCH). "
                f"Got: '{version}'"
            )
        else:
            result.add_pass("metadata.json: 'version' follows semver format")

    return metadata


def validate_pipeline_yaml(template_dir: Path, result: ValidationResult) -> dict | None:
    """Validate pipeline.yaml file."""
    pipeline_path = template_dir / "pipeline.yaml"

    if not pipeline_path.exists():
        result.add_error("pipeline.yaml: File not found (required)")
        return None

    # Check YAML syntax
    try:
        with open(pipeline_path, 'r') as f:
            pipeline = yaml.safe_load(f)
        result.add_pass("pipeline.yaml: Valid YAML syntax")
    except yaml.YAMLError as e:
        result.add_error(f"pipeline.yaml: Invalid YAML syntax - {e}")
        return None

    if not isinstance(pipeline, dict):
        result.add_error("pipeline.yaml: Root must be a mapping/object")
        return None

    # Check version field
    if 'version' not in pipeline:
        result.add_error("pipeline.yaml: Missing 'version' field at top level")
    elif pipeline['version'] != 1:
        result.add_warning(f"pipeline.yaml: Expected 'version: 1', got '{pipeline['version']}'")
    else:
        result.add_pass("pipeline.yaml: 'version: 1' present")

    # Check pipeline structure
    if 'pipeline' not in pipeline:
        result.add_error("pipeline.yaml: Missing 'pipeline' section")
        return pipeline

    pipeline_section = pipeline['pipeline']

    # Check stages
    if 'stages' not in pipeline_section:
        result.add_error("pipeline.yaml: Missing 'stages' in pipeline")
    else:
        stages = pipeline_section['stages']
        if not isinstance(stages, list):
            result.add_error("pipeline.yaml: 'stages' must be a list")
        else:
            stage_names = []
            for i, stage in enumerate(stages):
                if not isinstance(stage, dict):
                    result.add_error(f"pipeline.yaml: Stage {i} must be a mapping")
                    continue

                if 'name' not in stage:
                    result.add_error(f"pipeline.yaml: Stage {i} missing 'name' field")
                else:
                    stage_names.append(stage['name'])

                # Check for platform
                if 'platform' in stage:
                    platform = stage['platform']
                    if 'os' not in platform:
                        result.add_warning(f"pipeline.yaml: Stage '{stage.get('name', i)}' platform missing 'os'")
                    if 'arch' not in platform:
                        result.add_warning(f"pipeline.yaml: Stage '{stage.get('name', i)}' platform missing 'arch'")

                # Check steps
                if 'steps' in stage:
                    step_names = []
                    for j, step in enumerate(stage.get('steps', [])):
                        if not isinstance(step, dict):
                            continue
                        if 'name' not in step:
                            result.add_warning(f"pipeline.yaml: Step {j} in stage '{stage.get('name', i)}' missing 'name'")
                        else:
                            step_names.append(step['name'])

                        # Check for 'latest' tag in container images
                        if 'run' in step and isinstance(step['run'], dict):
                            run = step['run']
                            if 'container' in run and isinstance(run['container'], dict):
                                image = run['container'].get('image', '')
                                if image.endswith(':latest'):
                                    result.add_warning(
                                        f"pipeline.yaml: Step '{step.get('name', j)}' uses ':latest' tag. "
                                        "Consider using explicit version tags."
                                    )

                    # Check for duplicate step names within stage
                    duplicates = [name for name in step_names if step_names.count(name) > 1]
                    if duplicates:
                        result.add_error(
                            f"pipeline.yaml: Duplicate step names in stage '{stage.get('name', i)}': {set(duplicates)}"
                        )

            # Check for duplicate stage names
            duplicates = [name for name in stage_names if stage_names.count(name) > 1]
            if duplicates:
                result.add_error(f"pipeline.yaml: Duplicate stage names: {set(duplicates)}")
            else:
                result.add_pass("pipeline.yaml: All stage names are unique")

    # Check inputs section
    if 'inputs' in pipeline_section:
        inputs = pipeline_section['inputs']
        if isinstance(inputs, dict):
            result.add_pass(f"pipeline.yaml: {len(inputs)} inputs defined")

            for input_name, input_def in inputs.items():
                if not isinstance(input_def, dict):
                    result.add_warning(f"pipeline.yaml: Input '{input_name}' should be a mapping")
                    continue

                # Check for type field
                if 'type' not in input_def:
                    result.add_warning(f"pipeline.yaml: Input '{input_name}' missing 'type' field")
                elif input_def['type'] not in ['string', 'secret', 'connector']:
                    result.add_warning(
                        f"pipeline.yaml: Input '{input_name}' has unknown type '{input_def['type']}'. "
                        "Expected: string, secret, or connector"
                    )

                # Check for description (recommended)
                if 'description' not in input_def:
                    result.add_warning(f"pipeline.yaml: Input '{input_name}' missing description (recommended)")
    else:
        result.add_warning("pipeline.yaml: No 'inputs' section defined")

    return pipeline


def validate_wiki_md(template_dir: Path, result: ValidationResult, metadata: dict | None) -> None:
    """Validate wiki.MD file (optional)."""
    wiki_path = template_dir / "wiki.MD"

    if not wiki_path.exists():
        result.add_warning("wiki.MD: File not found (optional but recommended)")
        return

    try:
        with open(wiki_path, 'r') as f:
            content = f.read()
        result.add_pass("wiki.MD: File exists and is readable")
    except Exception as e:
        result.add_error(f"wiki.MD: Cannot read file - {e}")
        return

    # Check for title (# Agent Name)
    if not re.search(r'^#\s+.+', content, re.MULTILINE):
        result.add_error("wiki.MD: Missing title (# heading)")
    else:
        result.add_pass("wiki.MD: Title present")

    # Check for required sections
    required_sections = ['overview', 'key capabilities', 'inputs']
    content_lower = content.lower()

    for section in required_sections:
        # Look for section heading (## Section Name)
        if re.search(rf'^##\s+{section}', content_lower, re.MULTILINE):
            result.add_pass(f"wiki.MD: '{section}' section present")
        else:
            result.add_warning(f"wiki.MD: Missing '{section}' section (recommended)")

    # Check for code blocks with language specifiers
    code_blocks = re.findall(r'```(\w*)\n', content)
    unspecified = [i for i, lang in enumerate(code_blocks) if not lang]
    if unspecified:
        result.add_warning(f"wiki.MD: {len(unspecified)} code block(s) missing language specifier")
    else:
        result.add_pass("wiki.MD: All code blocks have language specifiers")


def validate_cross_file_consistency(
    template_dir: Path,
    result: ValidationResult,
    metadata: dict | None,
    pipeline: dict | None
) -> None:
    """Validate consistency across files."""
    if metadata is None or pipeline is None:
        return

    # Check that metadata name matches directory name pattern
    dir_name = template_dir.name
    expected_name = dir_name.replace('-', ' ')

    if metadata.get('name') == expected_name:
        result.add_pass("Cross-file: metadata.json 'name' matches directory name")


def validate_template(template_dir: Path) -> ValidationResult:
    """Validate a single template directory."""
    result = ValidationResult(template_dir.name)

    # Validate each file
    metadata = validate_metadata_json(template_dir, result)
    pipeline = validate_pipeline_yaml(template_dir, result)
    validate_wiki_md(template_dir, result, metadata)

    # Cross-file consistency
    validate_cross_file_consistency(template_dir, result, metadata, pipeline)

    return result


def find_templates(templates_dir: Path) -> list[Path]:
    """Find all template directories."""
    if not templates_dir.exists():
        return []

    templates = []
    for item in templates_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it looks like a template (has metadata.json or pipeline.yaml)
            if (item / "metadata.json").exists() or (item / "pipeline.yaml").exists():
                templates.append(item)

    return sorted(templates)


def main() -> int:
    """Main entry point."""
    # Determine templates directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    templates_dir = repo_root / "templates"

    # Allow specifying specific templates via command line
    if len(sys.argv) > 1:
        template_paths = [Path(arg) for arg in sys.argv[1:]]
    else:
        template_paths = find_templates(templates_dir)

    if not template_paths:
        print("No templates found to validate.")
        return 0

    print("=" * 60)
    print("Harness Agent Template Validation")
    print("=" * 60)
    print(f"\nValidating {len(template_paths)} template(s)...")

    results: list[ValidationResult] = []

    for template_path in template_paths:
        if not template_path.exists():
            print(f"\nWarning: Template path does not exist: {template_path}")
            continue

        result = validate_template(template_path)
        results.append(result)
        result.print_report()

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    passed = [r for r in results if r.is_valid()]
    failed = [r for r in results if not r.is_valid()]

    print(f"\nTemplates validated: {len(results)}")
    print(f"  Passed: {len(passed)}")
    print(f"  Failed: {len(failed)}")
    print(f"\nTotal errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")

    if failed:
        print("\nFailed templates:")
        for r in failed:
            print(f"  - {r.template_name}")
        print("\n❌ Validation FAILED")
        return 1
    else:
        print("\n✅ All templates passed validation")
        return 0


if __name__ == "__main__":
    sys.exit(main())
