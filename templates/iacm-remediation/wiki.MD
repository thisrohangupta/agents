# IaCM Remediation Agent

**Version:** 1.0.0
**Name:** IaCM Remediation

## Overview

The **IaCM Remediation Agent** is an AI-powered agent that automatically remediates infrastructure issues identified by Harness IaCM, STO, and CCM modules. It analyzes the issue, updates the source code in Terraform/OpenTofu repositories, and raises a pull request for review.

Supported remediation types:
- **iacm-drift**: Resolves infrastructure drift by updating source code to match the actual infrastructure state.
- **sto**: Fixes security vulnerabilities identified by Harness STO scans.
- **cloud-cost**: Applies cost optimization recommendations from Harness CCM.

---

## Key capabilities

- **Automatic drift detection**: Uses IaCM workspace configuration to run Terraform/OpenTofu `init` and `plan` commands and detect infrastructure drift automatically.

- **AI-powered code fixes**: Analyzes plan output to understand resource changes and updates `.tf` files to reflect actual infrastructure state with minimal, targeted changes.

- **Multi-type remediation**: Supports infrastructure drift remediation (`iacm-drift`), security vulnerability fixes (`sto`), and cloud cost optimization (`cloud-cost`).

- **Pull request automation**: Creates PRs with clear descriptions, submits for human review before any merge, and respects branch protection rules.

- **Context-aware reasoning**: Uses tfvar files and workspace variables for additional context, understands Terraform resource relationships and dependencies.

---

## How it works

1. **Init**: Runs `terraform/tofu init` using the IaCM workspace configuration.
2. **Plan**: Executes `terraform/tofu plan` to detect drift or changes.
3. **Remediation agent**: Analyzes the plan output and applies targeted code changes to resolve the issue.
4. **Show changes**: Displays `git diff` of applied fixes.
5. **Detect SCM and configure auth**: Derives repository information and credentials from the IaCM workspace (repo URL, token, branch, SCM provider).
6. **Push and create PR**: Commits changes, pushes to a new branch, and creates a pull request back to the source branch.

---

## Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `llmConnector` | connector | Yes | - | Anthropic API connector for Claude AI |
| `workspace` | string | Yes | - | IaCM workspace identifier |
| `remediationType` | string | No | `iacm-drift` | Type of remediation: `iacm-drift`, `sto`, or `cloud-cost` |
| `recommendation` | string | No | - | JSON string with recommendation details (required for `sto` and `cloud-cost` types) |


---

## Configuration

- **Platform**: Linux (arm64)
- **Timeout**: 10 minutes
- **Max iterations**: 200 (for coding agent)
- **Branch suffix**: `iacm-drift-remediation`
- **Force push**: Enabled
- **Unique per execution**: Yes (adds timestamp suffix)

---

## Usage example

### Basic usage (IaCM drift remediation)

```yaml
inputs:
  llmConnector: <select Anthropic connector>
  workspace: "my-workspace-id"
```

### STO remediation

```yaml
inputs:
  llmConnector: <select Anthropic connector>
  workspace: "my-workspace-id"
  remediationType: "sto"
  recommendation: '{"vulnerability": "CVE-2024-1234", "severity": "high", "fix": "upgrade package X to version Y"}'
```

### Cloud cost optimization

```yaml
inputs:
  llmConnector: <select Anthropic connector>
  workspace: "my-workspace-id"
  remediationType: "cloud-cost"
  recommendation: '{"resource": "aws_instance.web", "suggestion": "downsize from m5.xlarge to m5.large"}'
```

---

## Technical details

### IaCM remediation agent plugin
- **Container image**: `pkg.harness.io/.../iacm-remediation-agent-plugin`
- **Working directory**: Derived from `<+iacmOutput.rootDir>`
- **Inputs**: `ROOT_DIR`, `ANTHROPIC_API_KEY`, `PLUGIN_REMEDIATION_TYPE`, `PLUGIN_RECOMMENDATION`

### Create PR plugin
- **Container image**: `pkg.harness.io/.../create-pr-plugin`
- **Working directory**: Set via `PLUGIN_WORKING_DIR` (derived from IaCM workspace root)
- **Commit message**: "IaCM drift remediation: automated changes by Harness AI"

### Branch management
- **Branch name**: `<source-branch>-iacm-drift-remediation-<timestamp>`
- **Unique per execution**: Yes
- **Force push**: Enabled

### Pull request configuration
- **Auto-create**: Yes
- **PR title**: "IaCM Drift Remediation: Automated changes by Harness AI"
- **Draft mode**: Disabled
- **Bypass rules**: Disabled (respects branch protection rules)

### SCM provider support

Repository information (URL, token, branch, SCM type) is automatically derived from the IaCM workspace configuration. Supported providers:
- **GitHub**
- **GitLab**
- **Bitbucket**
- **Harness Code**

---

## Troubleshooting

### Init or plan fails
- Verify the IaCM workspace is correctly configured with valid provider credentials.
- Check that the workspace points to a valid Terraform/OpenTofu repository.

### Agent doesn't generate fixes
- Verify the `llmConnector` is properly configured with valid Anthropic credentials.
- Ensure the plan step detected changes.
- Check agent logs for error details.

### PR creation fails with "Not Found"
- Verify the repository information is correctly derived from the workspace.
- Check that the token has push and PR creation permissions.

### Authentication errors on git push
- The agent sets up authentication by embedding the workspace token in the git remote URL.
- Verify the workspace token has write access to the repository.

---

## Security considerations

- API keys are stored as Harness secrets and never exposed in logs.
- Agent only applies targeted fixes based on plan analysis.
- All changes are submitted via PR for human review.
- No automatic merging — requires developer approval.
- Respects branch protection rules (bypass disabled by default).

---

**Last updated:** March 2026
