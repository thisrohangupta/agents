# Code Review Agent

**Version:** 1.0.0  
**Name:** codereview

## Overview

An automated AI-powered agent that reviews code changes in pull requests and posts intelligent feedback using Anthropic's Claude API.

## How It Works

The agent operates in three stages:

1. **Review Prompt Generation** - Analyzes the PR and generates structured review instructions
2. **AI Code Review** - Claude AI performs comprehensive analysis (up to 50 iterations) examining code quality, bugs, security, and best practices
3. **Comment Posting** - Posts review feedback directly to the pull request via Harness SCM

## Required Inputs

| Input          | Type   | Description                          | Default                             |
| -------------- | ------ | ------------------------------------ | ----------------------------------- |
| `anthropicKey` | secret | API key for Anthropic's Claude API   | `account.autofix_anthropic_api_key` |
| `harnessKey`   | secret | Harness API key for posting comments | `account.harness_api_key`           |
| `repo`         | string | Repository name to review            | _Required_                          |
| `pullReq`      | string | Pull request identifier              | _Required_                          |
| `executionId`  | string | Unique execution identifier          | _Required_                          |

## Configuration

- **Clone Depth:** 100 commits
- **Platform:** Linux (amd64)
- **Max Iterations:** 50
- **Detailed Logging:** Enabled

## Usage Example

```yaml
inputs:
  repo: "my-organization/my-repository"
  pullReq: "123"
  executionId: "unique-execution-id-12345"
```

## Troubleshooting

- **Agent fails to start:** Verify API keys are configured correctly in Harness secrets
- **No comments posted:** Check `harnessKey` secret and ensure account ID is set in pipeline.yaml
- **Review incomplete:** Increase `max_iterations` or split PR into smaller changes

---

**Last Updated:** January 2026
