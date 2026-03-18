# Code Coverage Agent

**Version:** 1.0.0  
**Name:** Code Coverage

## Overview

The **Code Coverage Agent** is an AI-powered coding agent that automatically analyzes your codebase, identifies gaps in test coverage, and generates comprehensive unit tests to increase overall code coverage to at least 90%. Using Claude AI, it intelligently writes tests for files with low coverage, supporting multiple languages and testing frameworks including Go.

## Key Capabilities

- **🎯 Intelligent Test Generation**: Uses Claude Sonnet to analyze code and generate high-quality test cases
- **📊 Coverage Gap Analysis**: Identifies untested code paths and edge cases
- **✅ Automated Verification**: Built-in verification ensures tests meet quality standards
- **🔄 Smart Branch Management**: Creates unique branches per execution with automatic conflict handling
- **📝 Automated PR Creation**: Generates pull requests with descriptive titles and context
- **💬 Coverage Report Comments**: Automatically posts detailed coverage report as a PR comment
- **🔧 Multi-Language Support**: Works with various testing frameworks and languages (including Go)
- **🧪 Test Validation**: Verifies generated tests before creating PR
- **🌐 Multi-SCM Support**: Works with Harness Code, GitHub, GitLab, Bitbucket, and other Git providers

## How It Works

1. **Clone Repository**: Clones from the specified branch (default: main)
2. **Execute Coding Agent**: Runs Claude AI to analyze code and generate tests (up to 300 iterations)
3. **Generate Coverage Report**: Creates COVERAGE.md file with detailed coverage analysis
4. **Show Changes**: Displays git diff of added test files
5. **Detect SCM Provider**: Automatically identifies Git provider (Harness Code, GitHub, GitLab, etc.)
6. **Configure Authentication**: Sets up appropriate credentials based on SCM provider
7. **Push Changes**: Commits and pushes test additions to a unique branch
8. **Create PR**: Automatically creates a pull request back to the source branch
9. **Post Coverage Comment**: Adds a comment to the PR with the coverage report from COVERAGE.md

## Required Inputs

| Input | Type | Description | Default |
|-------|------|-------------|---------|
| `llmConnector` | connector | LLM connector for Claude AI (Anthropic) | _Required_ |
| `harnessKey` | secret | Harness API key for PR creation and commenting | `harness_api_key` |
| `gitConnector` | connector | Git connector for repository access | _Required_ |
| `repo` | string | Repository name to analyze | _Required_ |
| `branch` | string | Branch to clone from and create PR against | `main` |

## Configuration

- **Clone Depth:** 1 commit (shallow clone for performance)
- **Platform:** Linux (arm64)
- **Max Iterations:** 300
- **Detailed Logging:** Enabled
- **Code Coverage Mode:** Enabled
- **Verification:** Enabled
- **Coverage Target:** 90% overall coverage, 80% per file

## Agent Behavior

The agent is pre-configured with the following objective:

> "Analyze the current codebase and identify test coverage. Generate comprehensive unit tests to increase overall coverage to at least 90% and each file coverage to at least 80%. Generate a CONCISE COVERAGE.md file (under 10000 characters) with: Overall coverage percentage (before → after), Summary table of files modified/added with their coverage percentages, Files coverage percentage, Key improvements achieved, Use bullet points and tables for brevity - avoid lengthy explanations."

The agent will:
- Scan all source files in the repository
- Identify files with missing or insufficient test coverage
- Generate appropriate unit tests based on the language and framework detected
- Create a COVERAGE.md file with detailed coverage analysis
- Ensure tests follow best practices and coding standards
- Validate that generated tests pass before creating the PR
- Post the coverage report as a comment on the created PR

## Usage Example

```yaml
inputs:
  repo: "my-organization/my-repository"
  branch: "main"
```

The agent will automatically handle the rest, including SCM provider detection, authentication, branch creation, and PR submission.

## Technical Details

### Coding Agent Settings
- **Container Image**: `himanshu6956/codecov:coding-agent-with-go`
- **Max Iterations**: 300
- **Detailed Logging**: Enabled
- **Code Coverage Mode**: Enabled
- **Verification**: Enabled
- **Show Diff**: Disabled during execution (shown in separate step)
- **Working Directory**: `/harness`

### Branch Management
- **Branch Suffix**: `code-coverage-agent`
- **Unique Per Execution**: Yes (appends timestamp to avoid conflicts)
- **Force Push**: Enabled
- **Commit Message**: "Code coverage: automated test additions by Harness AI"

### Pull Request Configuration
- **Auto-Create**: Yes
- **PR Title**: "Code Coverage: Automated coverage increase by Harness AI"
- **PR Description**: "Automated code coverage improvements created by code-coverage-agent. Please review the generated tests before merging."
- **Draft Mode**: Disabled
- **Bypass Rules**: Disabled (respects branch protection rules)
- **Coverage Comment**: Automatically posts COVERAGE.md report as a PR comment

### SCM Provider Support

The agent automatically detects and configures authentication for:
- **Harness Code** (Git SCM type)
- **GitHub**
- **GitLab**
- **Bitbucket**
- Other Git providers

Authentication is handled transparently using the provided `gitConnector` and appropriate tokens.

## Best Practices

### Reviewing Generated Tests
- Always review the PR before merging
- Verify tests are meaningful and not just increasing coverage numbers
- Check that tests follow your team's conventions
- Ensure tests are maintainable and not brittle
- Validate that tests actually test the intended functionality

### Repository Requirements
- Ensure your repository has a testing framework configured
- Have a clear project structure that the agent can analyze
- Include any necessary test dependencies in your dependency files
- Configure coverage tools if you want to measure improvement

## Troubleshooting

### Agent Doesn't Generate Tests
- Verify the `llmConnector` is properly configured with valid Anthropic credentials
- Ensure the repository has accessible source code files
- Check that the repository structure is recognizable
- Review agent logs in the pipeline execution

### Tests Fail or Don't Pass
- Ensure test framework dependencies are installed in the repository
- Check if the testing framework is properly configured
- Verify that the build environment has all necessary dependencies
- Review the generated tests in the PR for any obvious issues

### No PR Created
- Verify `harnessKey` secret has correct permissions
- Check that changes were actually made (review git diff step)
- Ensure branch permissions allow PR creation
- Confirm the `gitConnector` is properly configured (if using external SCM)

### Coverage Comment Not Posted
- Check if COVERAGE.md file was generated by the coding agent
- Verify `harnessKey` has permissions to comment on PRs
- Review the `prepare_coverage_comment` step logs
- Ensure the PR was created successfully (PR_NUMBER is available)

### Authentication Errors
- Verify the `gitConnector` has valid credentials
- For Harness Code: Ensure `harnessKey` is valid
- For external SCMs: Verify the connector token has push permissions
- Check that the SCM provider is correctly detected in logs

### Branch Conflicts
- The agent creates unique branches per execution to avoid conflicts
- If issues persist, manually delete stale branches with the `code-coverage-agent` prefix
- Ensure force push is enabled (default configuration)

## Security Considerations

- API keys are stored as Harness secrets and never exposed in logs
- Agent only adds tests, doesn't modify production code
- All changes are submitted via PR for human review
- No automatic merging - requires developer approval
- Respects branch protection rules (bypass disabled by default)
- Authentication credentials are handled securely via netrc configuration

---

**Last Updated:** January 2026

