# Go upgrade

## Overview

The Go upgrade agent is an AI-powered coding agent that automates Go version upgrades in your repository. It updates `go.mod`, `go.sum`, Dockerfiles, CI configs, and code for breaking changes, then opens a pull request with the changes.

## Key capabilities

- **AI-powered Go upgrades**: Uses Claude to update Go version and fix breaking changes.
- **Full-repo scope**: Updates `go.mod`, `go.sum`, Dockerfiles, and CI that pin Go.
- **Automatic PR**: Creates a branch, commits, and opens a PR for review.
- **Custom prompts**: You specify the target version and scope via the prompt input.

## How it works

1. **Clone repository**: Clones from the specified branch (default: main).
2. **Run coding agent**: Runs the coding agent with your prompt and `go_upgrade` mode.
3. **Show changes**: Displays git diff of all modifications.
4. **Fix env variables**: Detects SCM provider and sets credentials for push.
5. **Push and create PR**: Pushes to a `go-upgrade-agent` branch and creates a PR to the source branch.

## Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| llmConnector | connector | Yes | - | LLM connector for Claude AI (Anthropic). |
| harnessKey | secret | No | harness_api_key | Harness API key for PR creation. |
| gitConnector | connector | Yes | - | Git connector for repository access. |
| repo | string | Yes | - | Repository name (e.g., my-service). |
| branch | string | No | main | The branch to clone from and create PR against. |
| prompt | string | Yes | - | The prompt for the coding agent (e.g., target Go version and scope). |

## Example prompts

### Upgrade to a specific version

```
Upgrade Go to 1.22. Update go.mod, go.sum, any Dockerfiles or CI that pin Go, and fix any breaking changes.
```

### Upgrade to latest stable

```
Upgrade Go to the latest stable version. Update go.mod, go.sum, Dockerfiles, and CI configs. Fix any breaking changes and run go mod tidy.
```

### Minimal scope

```
Upgrade the go directive in go.mod to 1.21 and run go mod tidy. Do not change Dockerfiles or CI.
```

## Example usage

```yaml
# In your pipeline inputs, set prompt to something like:
prompt: "Upgrade Go to 1.22. Update go.mod, go.sum, Dockerfiles, and CI. Fix breaking changes."
```

## Troubleshooting

### PR not created

- Ensure `harnessKey` has permissions to create PRs in your project.
- Check that the git connector has push access to the repo.

### No changes or wrong files updated

- Make the prompt more specific (e.g., list files or directories to touch).
- Include “run go mod tidy” if you want dependency cleanup.

### Build or tests fail after upgrade

- Review the agent’s diff and fix any missed breaking changes.
- Run tests locally or in CI before merging the PR.

### Coding agent errors

- Verify `llmConnector` is configured with valid Anthropic credentials.
- Ensure the delegate has network access to the LLM API.
