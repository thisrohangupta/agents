# Zero Day Remediation Agent

## Overview

The 0-Day Remediation agent automatically identifies and remediates critical vulnerabilities in your software supply chain. When a zero-day vulnerability is discovered, this agent inspects logs, test failures, and config errors, proposes concrete fixes, and automatically creates pull requests to downgrade to the safest compatible version.

---

## Key Benefits

- **Reduce Technical Debt**
  Automatically removes vulnerable packages and dead code, keeping your codebase clean and maintainable without manual intervention.

- **Automate Cleanup PRs**
  Generates ready-to-review pull requests with all package references removed, including code paths and related configurations.

- **Safe & Validated**
  Validates that packages are safe to remove by checking rollout states, targeting rules, and recent activity patterns.

- **Full Visibility**
  Track all cleanup actions through your pipeline with complete audit trails and approval workflows when needed.

---

## How It Works

1. **Scan & Detect**
   Agent scans your codebase and vulnerability databases to identify 0-day threats that affect your packages.

2. **Validate Safety**
   Verifies that detected packages are safe to remove by checking rollout percentages, targeting rules, and recent activity.

3. **Generate PR**
   Agent scans your entire codebase to find all references and creates pull requests that remove flag definitions, checks, and dead code.

4. **Review & Merge**
   Team reviews the automated PR through your standard process, with changes fully tested and validated before merging.

---

## Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| anthropicKey | secret | Yes | - | Anthropic API key for Claude LLM analysis |
| harnessKey | secret | Yes | - | Harness PAT token for API operations |
| repoAccessToken | secret | Yes | - | Git access token for repository operations |
| cveId | string | No* | - | CVE identifier to remediate (e.g., CVE-2021-44228) |
| componentName | string | No* | - | Vulnerable component name to upgrade |
| fixedVersion | string | No | - | Target version to upgrade to |
| currentVersion | string | No | - | Current vulnerable version |
| harnessOrgId | string | Yes | - | Harness organization ID |
| harnessProjectId | string | Yes | - | Harness project ID |
| targetBranch | string | No | main | Target branch for pull requests |
| branchPrefix | string | No | fix/ | Prefix for fix branches |
| authorName | string | No | AI Workflow | Git author name for commits |
| authorEmail | string | No | ai-workflow@harness.io | Git author email for commits |
| maxRepos | string | No | 0 | Maximum repositories to process (0 for unlimited) |
| search | string | No | - | Filter repositories by name pattern |

*Either `cveId` or `componentName` is required.

---

## Requirements

- Harness Supply Chain Security module enabled
- Repository access with write permissions
- Supported languages: Java, JavaScript, TypeScript, Python, Go, C#
- Git-based version control (GitHub, GitLab, Bitbucket)

---

## Example Usage

### CVE-Based Remediation

```yaml
- name: remediate_vulnerabilities
  run:
    container:
      image: harness/vulnerability-remediation-plugin:latest
    with:
      cve_id: "CVE-2021-44228"
      harness_org_id: "default"
      harness_project_id: "my-project"
      max_repos: "10"
      detailed_logging: "true"
    env:
      ANTHROPIC_API_KEY: <+inputs.anthropicKey>
      HARNESS_API_KEY: <+inputs.harnessKey>
      REPO_ACCESS_TOKEN: <+inputs.repoAccessToken>
```

### Component Upgrade

```yaml
- name: remediate_vulnerabilities
  run:
    container:
      image: harness/vulnerability-remediation-plugin:latest
    with:
      component_name: "log4j-core"
      fixed_version: "2.17.0"
      harness_org_id: "default"
      harness_project_id: "my-project"
      target_branch: "main"
      branch_prefix: "fix/"
    env:
      ANTHROPIC_API_KEY: <+inputs.anthropicKey>
      HARNESS_API_KEY: <+inputs.harnessKey>
      REPO_ACCESS_TOKEN: <+inputs.repoAccessToken>
```
