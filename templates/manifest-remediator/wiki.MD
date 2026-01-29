# Manifest Remediator Agent

## Overview

The **Manifest Remediator Agent** is an intelligent deployment failure recovery system that automatically analyzes Kubernetes and Helm deployment failures, generates targeted fixes, and produces remediation YAML files with actionable solutions. When deployment pipelines fail, the agent fetches logs, analyzes the root cause, and applies AI-powered fixes to manifest files and configurations.

The goal is to **accelerate deployment recovery**, **reduce mean-time-to-resolution (MTTR)**, and **automate manifest error corrections**—while maintaining safety and providing clear remediation documentation.

---

## Key Capabilities

- 🔍 **Intelligent Log Fetching**
  - Automatically fetches logs from your failed deployment steps
  - Focuses on K8sRollingDeploy and HelmDeploy failures
  - Gathers comprehensive context for accurate analysis

- 🛠 **AI-Powered Remediation**
  - Analyzes deployment failures using AI
  - Generates targeted fixes for manifest files and configurations
  - Provides minimal, scoped changes to resolve issues

- 📋 **Structured Output**
  - Creates detailed YAML file (`manifest_remediation_results.yaml`) with:
    - Root cause analysis
    - Recommended fixes and changes
    - Step-by-step remediation instructions
  - Provides real-time logging of each analysis phase

- 🧠 **Context-Aware Analysis**
  - Understands Kubernetes and Helm deployment patterns
  - Correlates errors with manifest configurations

---

## How It Works

1. **Analysis**
   - Fetches logs from your failed K8sRollingDeploy and HelmDeploy steps
   - Analyzes failures to identify root causes and manifest-specific issues

2. **Fix Generation**
   - Generates targeted remediation recommendations
   - Creates detailed `manifest_remediation_results.yaml` file

3. **Results Display**
   - Outputs the complete remediation YAML
   - Provides actionable next steps

---

## Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `anthropicKey` | secret | Yes | `autofix_anthropic_api_key` | Anthropic API key for Claude AI models |
| `harnessKey` | secret | Yes | `harness_api_key` | Harness API key for fetching logs and pipeline data |
| `harnessExecutionId` | string | Yes | - | Execution ID of the failed pipeline run |
| `harnessPipelineId` | string | Yes | - | Pipeline identifier containing the deployment |
| `harnessBaseUrl` | string | Yes | - | Harness base URL (e.g., `https://app.harness.io/gateway`) |
| `harnessProjectId` | string | Yes | - | Harness project identifier |
| `harnessOrgId` | string | Yes | - | Harness organization identifier |
| `harnessAccountId` | string | Yes | - | Harness account identifier |

---

## Prerequisites

Before running the agent, ensure you have:

- **Anthropic API Key**: Access to Claude AI models
- **Harness API Key**: Permissions to read pipeline execution logs
- **Failed Pipeline Execution**: The execution ID from a failed deployment

---

## Outputs

### Primary Output

**`manifest_remediation_results.yaml`** - Comprehensive YAML file containing:
- Detailed analysis of deployment failure
- Root cause identification
- Specific remediation steps
- Recommended manifest changes
- Configuration updates
- Deployment strategy adjustments

### Console Output

The agent will print:
- Progress updates as it analyzes your deployment
- The complete remediation YAML with recommendations
- Summary of findings and next steps

---

## Use Cases

### 1. Automated Deployment Recovery
- Analyze K8s deployment failures automatically
- Generate fixes for image pull errors, resource constraints, config issues
- Provide actionable remediation steps

### 2. Helm Chart Debugging
- Identify template rendering issues
- Detect value misconfigurations
- Suggest chart corrections

### 3. Manifest Validation
- Catch YAML syntax errors
- Identify missing required fields
- Validate resource specifications

### 4. Continuous Deployment Enhancement
- Integrate into post-deployment failure workflows
- Automate first-level incident response
- Reduce manual troubleshooting time

---

## Workflow

```
Failed Pipeline
      ↓
  Log Fetching
      ↓
  AI Analysis
      ↓
Remediation YAML
```

---

## Troubleshooting

### Common Issues

**Agent fails to start**
- Verify `anthropicKey` secret is configured and valid
- Check API key has sufficient credits/permissions

**No logs fetched**
- Ensure `harnessKey` has permissions to read pipeline logs
- Verify the execution ID and pipeline ID are correct
- Check that your pipeline contains K8sRollingDeploy or HelmDeploy steps

**Remediation YAML not generated**
- Review the agent logs in the pipeline output
- Ensure the failed step had actionable error information

**API connection failures**
- Verify `harnessBaseUrl` is correct (e.g., `https://app.harness.io/gateway`)
- Ensure all Harness IDs match your execution context

**Missing API keys**
- Configure both `anthropicKey` and `harnessKey` as secrets in your pipeline

---

## Optional Settings

You can customize the agent behavior with:

- `detailed_logging`: Set to `"true"` for verbose output

---

## Supported Deployment Types

This agent works with:
- Kubernetes Rolling Deployments (K8sRollingDeploy)
- Helm Deployments (HelmDeploy)
- Kubernetes manifest-based deployments
- Helm chart deployments

---

**Version:** 1.0.0  
**Last Updated:** January 2026
