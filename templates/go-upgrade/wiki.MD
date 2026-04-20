# Go upgrade

## Overview

The Go upgrade agent is an AI-powered coding agent that automates Go version upgrades in your repository. It updates `go.mod`, `go.sum`, Dockerfiles, CI configs, and code for breaking changes, then opens a pull request with the changes.

## Key capabilities

- **AI-powered Go upgrades**: Uses Claude to update Go version and fix breaking changes.
- **Full-repo scope**: Updates `go.mod`, `go.sum`, Dockerfiles, and CI that pin Go.
- **Automatic PR**: Creates a branch, commits, and opens a PR for review.
- **Build and test verification**: Runs `go build ./...` and `go test ./...` before creating the PR so the pipeline fails if the upgrade breaks the project.
- **Custom prompts**: You specify the target version and scope via the prompt input.

## How it works

1. **Clone repository**: Clones from the specified branch (default: main).
2. **Run coding agent**: Runs the coding agent with your prompt and `go_upgrade` mode.
3. **Show changes**: Displays git diff of all modifications.
4. **Go build**: Runs `go build ./...` in a Go container to verify the project compiles.
5. **Go test**: Runs `go test ./...` in a Go container to verify tests pass.
6. **Fix env variables**: Detects SCM provider and sets credentials for push.
7. **Push and create PR**: Pushes to a `go-upgrade-agent` branch and creates a PR to the source branch.

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

### Recommended prompt (best outcome)

Use this prompt to get consistent, well-documented upgrades. It guides the agent through analysis, version decision, upgrade execution, verification, and PR content. Replace `/harness/drone-s3` with your repo path (e.g. `/harness` or the relevant subpath).

```text
You are a CI/CD automation agent responsible for upgrading Go SDK versions in a repository to fix vulnerabilities and update dependencies. Your goal is to analyze the current state, perform the upgrade intelligently, verify the changes work correctly, and create a pull request with clear documentation. Here is the repository context you'll be working with: /harness/drone-s3. Follow these steps to complete the upgrade process: ## Step 1: Analysis Phase First, analyze the repository to understand the current Go setup. Use a <analysis> section to document your findings: - Identify the current Go version being used - Locate all places where the Go version is defined (go.mod file, CI/CD YAML files like .github/workflows, .gitlab-ci.yml, Dockerfiles, etc.) - Note the current dependencies in go.mod and go.sum - Identify any version constraints or special configurations Write your analysis inside <analysis> tags, documenting each finding clearly. ## Step 2: Version Decision Phase Use a <version_decision> section to think through and decide on the target Go version: - Check the latest stable Go version available (you should fetch this information in real-time if possible, or use your knowledge of recent stable releases) - Review the upgrade requirements provided by the user - If the user specified a target version in the upgrade requirements, use that version - If no specific version was mentioned, determine the best version to upgrade to by considering: - The current version and how far behind it is - Whether to do a minor version upgrade or major version upgrade - Stability and LTS considerations - Common compatibility issues between versions - Document your reasoning and final decision Write your version decision and reasoning inside <version_decision> tags. ## Step 3: Upgrade Execution Phase Now perform the actual upgrade. Document your actions in an <upgrade_actions> section: 1. Update the Go version in go.mod file (the `go` directive) 2. Update the Go version in all CI/CD configuration files you identified 3. Update any Dockerfiles or other configuration files that specify Go version 4. Run `go mod tidy` to update go.sum and clean up dependencies 5. Check if any dependencies need updating due to the Go version change List each file you're modifying and the specific changes made inside <upgrade_actions> tags. ## Step 4: Verification Phase Test that the upgrade works correctly. Use a <verification> section with iterative problem-solving: 1. Run `go build` to ensure the code compiles 2. Run `go test ./...` to ensure all tests pass 3. If either command fails: - Analyze the error messages in a <error_analysis> subsection - Determine the root cause (dependency incompatibility, deprecated API usage, etc.) - Apply fixes (update dependencies, modify code if necessary) - Re-run the verification steps - Repeat this loop until both build and tests succeed Document all verification attempts, any errors encountered, fixes applied, and final success inside <verification> tags. If you need to iterate, show each iteration clearly. ## Step 5: Pull Request Creation Phase Create a comprehensive pull request. Structure your PR content in these sections: <pr_title> Write a clear, concise title that follows this format: "chore: upgrade Go to [version] to address vulnerabilities" or "chore: upgrade Go from [old_version] to [new_version]" </pr_title> <pr_description> Write a detailed PR description that includes: **Why**: - Explain the reason for the upgrade (security vulnerabilities, dependency updates, etc.) - Reference any specific CVEs or security issues if applicable **What Changed**: - List the Go version change (from X to Y) - Summarize files modified (go.mod, CI configs, etc.) - Note any dependency updates from go mod tidy - Mention any code changes made to fix compatibility issues **Verification**: - Confirm that `go build` succeeds - Confirm that `go test` passes - Note any additional testing performed **Files Modified**: - Provide a bullet list of all files changed and why </pr_description> ## Important Guidelines: - Be thorough in your analysis before making changes - Always verify changes work before creating the PR - If you encounter errors during verification, do not give up - iterate and fix them - Be explicit about what you're changing and why - If you cannot access real-time information about the latest Go versions, use your most recent knowledge and note this limitation - Ensure go.sum is properly updated with `go mod tidy` after any go.mod changes - Consider backward compatibility when making version jumps Provide your complete response with all the tagged sections above, working through each phase systematically.
```

### Short prompts

**Upgrade to a specific version**

```
Upgrade Go to 1.22. Update go.mod, go.sum, any Dockerfiles or CI that pin Go, and fix any breaking changes.
```

**Upgrade to latest stable**

```
Upgrade Go to the latest stable version. Update go.mod, go.sum, Dockerfiles, and CI configs. Fix any breaking changes and run go mod tidy.
```

**Minimal scope**

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
