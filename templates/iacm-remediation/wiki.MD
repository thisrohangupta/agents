# IaCM Remediation Agent

**Version:** 1.0.0
**Name:** IaCM Remediation

## Overview

The **IaCM Remediation Agent** is an AI-powered agent that automatically detects and fixes infrastructure drift in Terraform and OpenTofu repositories. The agent first runs `terraform/tofu plan` to detect drift, and if found, analyzes the plan to understand the discrepancies and updates the source code to match the real infrastructure state — then raises a pull request for review.

---

## Key Capabilities

- 🔍 **Automatic Drift Detection**

  - Runs Terraform/OpenTofu `init` and `plan` commands
  - Detects infrastructure drift automatically
  - Generates plan JSON for analysis
  - Skips remediation when no drift is detected (exit code 0)

- 📊 **Drift Analysis**

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
  - Uses tfvar files for additional context when available
  - Understands Terraform resource relationships and dependencies
  - Applies minimal, targeted changes to resolve drift

---

## How It Works

1. **Clone Repository**: Clones the Terraform/OpenTofu repository from the specified branch
2. **Bootstrap & Drift Detection**: Runs `terraform/tofu init` and `plan` to detect drift
   - Exit Code 0: No drift detected → Pipeline completes successfully
   - Exit Code 10: Drift detected → Continues to remediation
3. **IaCM Remediation Agent**: (Only if drift detected) Analyzes the plan JSON and applies code changes to resolve drift
4. **Show Changes**: Displays git diff of applied fixes
5. **Detect SCM Provider**: Automatically identifies Git provider (Harness Code, GitHub, GitLab, etc.)
6. **Configure Authentication**: Sets up appropriate credentials based on SCM provider
7. **Push Changes**: Commits and pushes fixes to the `iacm-drift-remediation` branch
8. **Create PR**: Automatically creates a pull request back to the source branch

## Required Inputs

| Input | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| `llmConnector` | connector | Yes | LLM connector for Claude AI (Anthropic) | _Required_ |
| `awsConnector` | connector | Yes | AWS connector for infrastructure access | _Required_ |
| `harnessKey` | secret | No | Harness API key for PR creation | `harness_api_key` |
| `gitConnector` | connector | Yes | Git connector for repository access | _Required_ |
| `repo` | string | Yes | Repository name | _Required_ |
| `branch` | string | No | Branch to clone from and create PR against | `main` |
| `repoType` | string | No | Repository type: `terraform` or `opentofu` | `opentofu` |
| `awsRegion` | string | No | AWS region for infrastructure | `us-east-1` |
| `tfvarFile` | string | No | Path to tfvar file (relative to repo root) for plan and context | — |

## Configuration

- **Clone Depth:** 1 commit (shallow clone for performance)
- **Platform:** Linux (arm64)
- **Max Iterations:** 200 (for coding agent)
- **Detailed Logging:** Enabled
- **Branch Name:** `iacm-drift-remediation`
- **Force Push:** Enabled

## Agent Behavior

The IaCM remediation workflow operates in two phases:

### Phase 1: Bootstrap & Detection
1. **Init**: Runs `terraform/tofu init` to initialize the workspace
2. **Plan**: Executes `terraform/tofu plan` with optional tfvar file
3. **Drift Detection**: Analyzes plan JSON for resource changes
4. **Decision**:
   - No drift (exit code 0) → Pipeline ends successfully
   - Drift detected (exit code 10) → Proceeds to Phase 2

### Phase 2: Remediation (Conditional)
1. **Prompt Construction**: References the plan.json file and optional tfvar file
2. **AI Code Agent Execution**: The `ai-code-agent` binary reads the plan, analyzes the drift, and makes targeted changes to `.tf` files
3. **Change Submission**: All changes are committed, pushed, and submitted as a PR for review

The agent focuses exclusively on resolving the drift detected in the plan. It does not make speculative changes or modify resources that are not part of the drift.

## Usage Example

### Basic Usage (OpenTofu with AWS)

```yaml
inputs:
  llmConnector: <select Anthropic connector>
  awsConnector: <select AWS connector>
  gitConnector: <select Git connector>
  repo: "my-organization/my-terraform-repo"
  branch: "main"
  repoType: "opentofu"
  awsRegion: "us-east-1"
```

### With Terraform and Tfvar File

```yaml
inputs:
  llmConnector: <select Anthropic connector>
  awsConnector: <select AWS connector>
  gitConnector: <select Git connector>
  repo: "my-organization/my-terraform-repo"
  branch: "main"
  repoType: "terraform"
  awsRegion: "us-west-2"
  tfvarFile: "environments/prod.tfvars"
```

### Multiple Environments

```yaml
inputs:
  llmConnector: <select Anthropic connector>
  awsConnector: <select AWS connector>
  gitConnector: <select Git connector>
  repo: "my-organization/my-terraform-repo"
  branch: "staging"
  repoType: "opentofu"
  awsRegion: "eu-west-1"
  tfvarFile: "terraform.staging.tfvars"
```

## Technical Details

### IaCM Bootstrap Agent Settings
- **Container Image**: `sunnyagarwalhs/iacm-bootstrap-agent:latest`
- **Working Directory**: `/harness`
- **Output Directory**: `/harness/drift-output`
- **Plan Output**: `plan.json`
- **Output Variables**:
  - `DRIFT_DETECTED="false"` = No drift
  - `DRIFT_DETECTED="true"` = Drift detected

### IaCM Remediation Agent Settings
- **Container Image**: `sunnyagarwalhs/iacm-remediation-agent:latest`
- **Working Directory**: `/harness`
- **Plan File**: `/harness/drift-output/plan.json`
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

### Tfvar Files
- Specify the tfvar file path relative to repository root
- The same tfvar file is used for both plan generation and remediation context
- Supports any `.tfvars` file in your repository structure
- Example paths: `terraform.tfvars`, `environments/prod.tfvars`, `vars/production.tfvars`

### Cloud Provider Access
- Use Harness connectors for cloud provider authentication
- The bootstrap agent requires read access to infrastructure state
- For AWS: Provide an AWS connector with appropriate IAM permissions
- The connector credentials are automatically set as environment variables for Terraform/OpenTofu
- Supported providers: AWS (more providers can be added as needed)

## Troubleshooting

### Bootstrap Agent Fails
- Verify that your repository contains valid Terraform/OpenTofu files
- Ensure required provider credentials are available
- Check that the `tfvarFile` path is correct (if specified)
- Review bootstrap logs for initialization or planning errors

### Agent Doesn't Generate Fixes
- Verify the `llmConnector` is properly configured with valid Anthropic credentials
- Ensure the bootstrap agent successfully generated plan.json
- Check that the repository contains `.tf` files the agent can modify
- Review agent logs in the pipeline execution for error details

### Fixes Don't Resolve the Drift
- Try providing a `tfvarFile` for additional context
- Review the agent's changes to understand its reasoning
- Verify the plan was generated against current infrastructure
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
