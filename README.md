Note: This repo will eventually be moved into harness/

# System Agent Templates

This repository stores all system agent templates for Harness agents.

## 📋 Table of Contents

- [Overview](#overview)
- [Template Structure](#template-structure)
- [Adding a New Template](#adding-a-new-template)
- [Template Registration](#template-registration)
- [File Format Reference](#file-format-reference)
- [Best Practices](#best-practices)

---

## Overview

Agent templates are modular pipeline definitions that encapsulate:

- **Pipeline configuration** (stages, steps, containers, inputs)
- **Metadata** (name, description, version)
- **Documentation** (usage guides, capabilities, examples)

The Agents service automatically discovers and registers templates from this repository, making them available for deployment and execution.

---

## Template Structure

Each template must be organized in its own directory under `templates/` with the following files:

```
templates/
└── <template-name>/
    ├── metadata.json      # Template metadata and versioning (required)
    ├── pipeline.yaml      # Pipeline definition and configuration (required)
    ├── wiki.MD            # User-facing documentation (optional)
    └── logo.svg           # Template logo/icon (optional)
```

### Example Structure

```
templates/
└── autofix/
    ├── metadata.json
    ├── pipeline.yaml
    ├── wiki.MD
    └── logo.svg
```

---

## Adding a New Template

Follow these steps to add a new agent template:

### 1. Create Template Directory

Create a new directory under `templates/` with your agent's name (use lowercase, hyphen-separated names):

```bash
mkdir -p templates/my-agent
```

### 2. Create Required Files

#### **metadata.json**

Define your template's metadata:

```json
{
  "name": "my-agent",
  "description": "Brief description of what this agent does",
  "version": "1.0.0"
}
```

#### **pipeline.yaml**

Define your pipeline configuration with inputs, stages, and steps:

```yaml
pipeline:
  clone:
    depth: 1
    ref:
      name: <+inputs.branch>
      type: branch
  repo:
    name: <+inputs.repo>
  stages:
    - name: my-agent-stage
      steps:
        - name: my-agent-step
          run:
            container:
              image: your-registry/your-image:tag
            env:
              PLUGIN_CONFIG_VAR: <+inputs.configVar>
              API_KEY: <+inputs.apiKey>
      platform:
        os: linux
        arch: amd64
  inputs:
    apiKey:
      type: secret
    configVar:
      type: string
      default: "default-value"
    repo:
      type: string
    branch:
      type: string
      default: main
```

#### **wiki.MD**

Create comprehensive documentation for your agent:

```markdown
# My Agent

## Overview

Brief description of what the agent does and why it's useful.

## Key Capabilities

- Feature 1
- Feature 2
- Feature 3

## Usage

How to use this agent, including:

- Prerequisites
- Configuration requirements
- Example workflows

## Inputs

| Input     | Type   | Required | Default         | Description                |
| --------- | ------ | -------- | --------------- | -------------------------- |
| apiKey    | secret | Yes      | -               | API key for authentication |
| configVar | string | No       | "default-value" | Configuration parameter    |

## Examples

Practical examples of using the agent.
```

#### **logo.svg** (Optional)

Provide an SVG logo for your agent to enhance visual identification in the UI:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <!-- Your logo design here -->
  <circle cx="50" cy="50" r="40" fill="#0066cc"/>
</svg>
```

**Logo Guidelines:**

- Use SVG format for scalability
- Keep dimensions square (e.g., 100x100, 200x200)
- Use simple, recognizable designs
- Avoid overly complex graphics

### 3. Commit and Push

```bash
git add templates/my-agent/
git commit -m "Add my-agent template"
git push origin main
```

---

## Template Registration

### How Templates Are Discovered

The Agents service automatically discovers and registers templates through the following process:

1. **Repository Polling**: The service periodically scans the `templates/` directory in this repository
2. **Validation**: Each template directory is validated for required files (`metadata.json`, `pipeline.yaml`)
3. **Metadata Extraction**: Template metadata is parsed from `metadata.json`
4. **Optional Files**: If present, `wiki.MD` and `logo.svg` are loaded for enhanced documentation and UI display
5. **Registration**: Valid templates are registered in the service catalog
6. **Availability**: Registered templates become available for deployment via API/UI

### Registration Requirements

For successful registration, templates must:

- ✅ Have required files: `metadata.json` and `pipeline.yaml`
- ✅ Use valid JSON in `metadata.json`
- ✅ Use valid YAML in `pipeline.yaml`
- ✅ Include a unique template name (no duplicates)
- ✅ Follow semantic versioning (e.g., `1.0.0`, `2.1.3`)

Optional enhancements:

- 📝 Include `wiki.MD` for detailed documentation
- 🎨 Include `logo.svg` for visual branding in the UI

### Versioning and Updates

- **Version Changes**: Update the `version` field in `metadata.json` when making changes
- **Backward Compatibility**: Avoid breaking changes to existing inputs/outputs
- **Deprecation**: Mark deprecated versions in the wiki documentation before removal

---

## File Format Reference

### metadata.json

**Required fields:**

```json
{
  "name": "string", // Template identifier (lowercase, alphanumeric, hyphens)
  "description": "string", // Brief description (1-2 sentences)
  "version": "string" // Semantic version (MAJOR.MINOR.PATCH)
}
```

### pipeline.yaml

The pipeline configuration follows the Harness CI pipeline v1 YAML format:

### wiki.MD (Optional)

Provides user-facing documentation for the agent template. When present, this is displayed in the UI and helps users understand how to use the agent.

**Recommended sections:**

1. **Overview**: What the agent does and its purpose
2. **Key Capabilities**: Main features and functionality
3. **Usage**: How to deploy and run the agent
4. **Inputs**: Detailed input parameter documentation
5. **Outputs**: Expected outputs and artifacts
6. **Examples**: Real-world usage examples
7. **Troubleshooting**: Common issues and solutions

### logo.svg (Optional)

---

## Best Practices

### Naming Conventions

- ✅ Use Sentence Case: `My Agent`, `Code Coverage`, `Library Upgrade`, `Autofix`, `Manifest Rendering`
- ❌ Avoid: `MyAgent`, `my_agent`, `MYAGENT`, `my-agent`, `code-scanner`

### Documentation

- Write clear, concise descriptions
- Include practical examples
- Document all inputs with types and defaults
- Explain expected behavior and outputs

### Security

- Never hardcode secrets or credentials
- Use `type: secret` for sensitive inputs
- Follow principle of least privilege
- Document security requirements in wiki
