# IaCM Remediation Agent

**Version:** 1.0.0
**Name:** IaCM Remediation

## Overview

The **IaCM Remediation Agent** is an AI-powered agent that automatically fixes infrastructure drift in Terraform and OpenTofu repositories. When your actual infrastructure state diverges from the code, the agent analyzes the drifted plan JSON, understands the discrepancies, and updates the source code to match the real infrastructure state — then raises a pull request for review.

---

## Key Capabilities

- 🔍 **Drift Analysis**

  - Parses Terraform/OpenTofu plan JSON to identify drifted resources
  - Understands resource attribute changes, additions, and removals
  - Correlates drift with existing source code definitions

- 🛠 **Automated Code Fixes**

  - Updates `.tf` files to reflect actual infrastructure state
  - Handles resource attribute changes (e.g., instance sizes, tags, configurations)
  - Respects existing code style and module structure

- 🔁 **Pull Request Automation**

  - Creates PRs with clear descriptions of drift remediation
  - Links changes back to the drifted resources
  - Submits for human review before any merge

- 🧠 **Context-Aware Reasoning**
  - Uses tfvar content for additional context when available
  - Understands Terraform resource relationships and dependencies
  - Applies minimal, targeted changes to resolve drift

---

## How It Works

1. **Clone Repository**: Clones the Terraform/OpenTofu repository from the specified branch
2. **IaCM Remediation Agent**: Analyzes the drifted plan JSON and tfvar content, then applies code changes to resolve drift
3. **Show Changes**: Displays git diff of applied fixes
4. **Detect SCM Provider**: Automatically identifies Git provider (Harness Code, GitHub, GitLab, etc.)
5. **Configure Authentication**: Sets up appropriate credentials based on SCM provider
6. **Push Changes**: Commits and pushes fixes to the `iacm-drift-remediation` branch
7. **Create PR**: Automatically creates a pull request back to the source branch

## Required Inputs

| Input | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| `llmConnector` | connector | Yes | LLM connector for Claude AI (Anthropic) | _Required_ |
| `harnessKey` | secret | No | Harness API key for PR creation | `harness_api_key` |
| `gitConnector` | connector | Yes | Git connector for repository access | _Required_ |
| `repo` | string | Yes | Repository name | _Required_ |
| `branch` | string | No | Branch to clone from and create PR against | `main` |
| `planJson` | string | Yes | The drifted Terraform/OpenTofu plan in JSON format | _Required_ |
| `tfvarContent` | string | No | Optional tfvar file content for additional context | — |

## Configuration

- **Clone Depth:** 1 commit (shallow clone for performance)
- **Platform:** Linux (arm64)
- **Max Iterations:** 200 (for coding agent)
- **Detailed Logging:** Enabled
- **Branch Name:** `iacm-drift-remediation`
- **Force Push:** Enabled

## Agent Behavior

The IaCM remediation agent works in a single stage:

1. **Prompt Construction**: Combines the drifted plan JSON and optional tfvar content into a structured prompt
2. **AI Code Agent Execution**: The `ai-code-agent` binary analyzes the prompt against the repository source code and makes targeted changes to `.tf` files to resolve the drift
3. **Change Submission**: All changes are committed, pushed, and submitted as a PR for review

The agent focuses exclusively on resolving the drift described in the plan JSON. It does not make speculative changes or modify resources that are not part of the drift.

## Usage Example

### Basic Usage (Plan JSON Only)

```yaml
inputs:
  repo: "my-organization/my-terraform-repo"
  branch: "main"
  planJson: |
    {
      "format_version": "1.2",
      "resource_changes": [
        {
          "address": "aws_instance.web",
          "change": {
            "actions": ["update"],
            "before": { "instance_type": "t2.large" },
            "after": { "instance_type": "t2.micro" }
          }
        }
      ]
    }
```

### With Tfvar Content

```yaml
inputs:
  repo: "my-organization/my-terraform-repo"
  branch: "main"
  planJson: |
    {
      "format_version": "1.2",
      "resource_changes": [
        {
          "address": "aws_instance.web",
          "change": {
            "actions": ["update"],
            "before": { "instance_type": "t2.large" },
            "after": { "instance_type": "t2.micro" }
          }
        }
      ]
    }
  tfvarContent: |
    instance_type = "t2.large"
    environment   = "production"
```

## Technical Details

### IaCM Remediation Agent Settings
- **Container Image**: `anewdocker25/mydockerhub:iacm-remediation-agent`
- **Working Directory**: `/harness`
- **Detailed Logging**: Enabled
- **Max Iterations**: 200

### Branch Management
- **Branch Name**: `iacm-drift-remediation`
- **Unique Per Execution**: Yes (adds timestamp suffix if branch exists)
- **Force Push**: Enabled
- **Commit Message**: "IaCM drift remediation: automated changes by Harness AI"

### Pull Request Configuration
- **Auto-Create**: Yes
- **PR Title**: "IaCM Drift Remediation: Automated changes by Harness AI"
- **PR Description**: "Automated infrastructure drift remediation for Terraform/OpenTofu. The source code has been updated to match the actual infrastructure state. Please review the changes before merging."
- **Draft Mode**: Disabled
- **Bypass Rules**: Disabled (respects branch protection rules)

### SCM Provider Support

The agent automatically detects and configures authentication for:
- **Harness Code** (Git SCM type)
- **GitHub**
- **GitLab**
- **Bitbucket**
- Other Git providers

Authentication is handled transparently using the provided `gitConnector` and appropriate tokens.

## Best Practices

### Reviewing Generated Fixes
- Always review the PR before merging
- Verify the drift resolution matches your intended infrastructure state
- Check that no unrelated resources were modified
- Run `terraform plan` after merging to confirm drift is resolved
- Ensure the changes align with your team's Terraform conventions

### Plan JSON Quality
- Use the full plan JSON output from `terraform plan -json` or `tofu plan -json`
- Include all resource changes, not just a subset
- Ensure the plan JSON is from a recent run against actual infrastructure

### Tfvar Content
- Provide tfvar content when your Terraform configuration uses variables
- This helps the agent understand which values come from variables vs. hardcoded values
- Include all relevant `.tfvars` content for accurate remediation

## Troubleshooting

### Agent Doesn't Generate Fixes
- Verify the `llmConnector` is properly configured with valid Anthropic credentials
- Ensure the `planJson` input contains valid Terraform plan JSON
- Check that the repository contains `.tf` files the agent can modify
- Review agent logs in the pipeline execution for error details

### Fixes Don't Resolve the Drift
- The plan JSON may not contain enough context for accurate remediation
- Try providing `tfvarContent` for additional context
- Review the agent's changes to understand its reasoning
- Manual intervention may be required for complex drift scenarios

### No PR Created
- Verify `harnessKey` secret has correct permissions
- Check that changes were actually made (review git diff step)
- Ensure branch permissions allow PR creation
- Confirm the `gitConnector` is properly configured

### Authentication Errors
- Verify the `gitConnector` has valid credentials
- For Harness Code: Ensure `harnessKey` is valid
- For external SCMs: Verify the connector token has push permissions
- Check that the SCM provider is correctly detected in logs

## Security Considerations

- API keys are stored as Harness secrets and never exposed in logs
- Agent only applies targeted fixes based on drift analysis
- All changes are submitted via PR for human review
- No automatic merging — requires developer approval
- Respects branch protection rules (bypass disabled by default)
- Plan JSON and tfvar content are passed as pipeline inputs, not stored persistently

---

**Last Updated:** February 2026
