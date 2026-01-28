# React Upgrade Agent

## Overview

The React Upgrade Agent is an AI-powered coding agent that automates React version upgrades and other code modifications using Claude AI. It accepts custom prompts to perform intelligent code changes, automatically creates branches, commits changes, and opens pull requests.

## Key Capabilities

- **AI-Powered Code Modifications**: Uses Claude Sonnet to make intelligent code changes based on your prompt
- **Flexible Task Execution**: Accepts any prompt for React upgrades, refactoring, or code improvements
- **Automatic Branch Management**: Creates unique branches with conflict detection
- **Smart PR Creation**: Automatically generates pull requests with your changes
- **Git Integration**: Handles commits, pushes, and branch management automatically
- **Dynamic Environment Support**: Works across different Harness environments

## How It Works

1. **Clone Repository**: Clones from the specified branch (default: main)
2. **Execute Coding Agent**: Runs Claude AI with your custom prompt to make code changes
3. **Show Changes**: Displays git diff of modifications
4. **Commit Changes**: Commits modifications with descriptive message
5. **Create Branch**: Creates `react-upgrade-code-agent` branch (or with timestamp if exists)
6. **Push to Remote**: Pushes the new branch to origin
7. **Create PR**: Automatically creates a pull request back to the source branch

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| anthropicKey | secret | Yes (default provided) | Anthropic API key for Claude AI (default: `autofix_anthropic_api_key`) |
| harnessKey | secret | Yes (default provided) | Harness API key for PR creation (default: `harness_api_key`) |
| gitConnector | connector | Yes | Git connector for repository access |
| repo | string | Yes | Repository name (e.g., `hello-world`) |
| branch | string | No | Branch to work on and create PR against (default: `main`) |
| prompt | string | Yes | **Custom prompt for the coding agent** - describe what changes you want |

## Environment Variables

The agent automatically receives these from Harness CI:
- `HARNESS_ACCOUNT_ID` - Account identifier
- `HARNESS_ORG_ID` - Organization identifier
- `HARNESS_PROJECT_ID` - Project identifier
- `DRONE_REPO_NAME` - Full repository path
- `DRONE_SYSTEM_HOST` - Harness instance hostname
- `DRONE_SYSTEM_PROTO` - Protocol (https)

## Example Prompts

### React Version Upgrade
```
Upgrade React from version 17 to 18. Update package.json, 
fix deprecated lifecycle methods, and ensure all tests pass.
```

### Code Refactoring
```
Refactor all class components to functional components with hooks.
Maintain the same functionality and props.
```

### Dependency Update
```
Update all React-related dependencies to their latest compatible versions.
Fix any breaking changes in the code.
```

### Performance Optimization
```
Add React.memo to all components that don't need frequent re-renders.
Optimize expensive computations with useMemo.
```

## Example Pipeline Usage

```yaml
version: 1
pipeline:
  clone:
    depth: 1
    ref:
      name: <+inputs.branch>
      type: branch
    repo: <+inputs.repo>
    connector: "<+inputs.gitConnector != null ? inputs.gitConnector.id : ''"
  stages:
    - name: react_upgrade
      steps:
        - name: coding_agent
          run:
            container:
              image: anewdocker25/mydockerhub:coding-agent
            with:
              prompt: "Upgrade React from 17 to 18 and fix breaking changes"
              max_iterations: "300"
              detailed_logging: "true"
            env:
              ANTHROPIC_API_KEY: <+inputs.anthropicKey>
```

## Branch Naming

The agent creates branches with the following logic:
- **Base name**: `react-upgrade-code-agent`
- **If branch exists**: Adds timestamp suffix (e.g., `react-upgrade-code-agent-1769583910`)
- This ensures no branch name conflicts

## Pull Request Flow

1. **Source Branch**: `react-upgrade-code-agent` (or with timestamp)
2. **Target Branch**: The branch you specified in `branch` input
3. **PR Title**: "React Upgrade: Automated changes"
4. **PR Description**: "Automated React upgrade changes created by react-upgrade-code-agent. Please review the changes before merging."

**Example**: If you run on `main`, PR will be `react-upgrade-code-agent` → `main`

## Configuration Options

The coding agent accepts these parameters via `with`:
- `prompt` - Your custom task description (required)
- `max_iterations` - Maximum iterations (default: 300)
- `detailed_logging` - Enable verbose logging (default: true)
- `working_directory` - Working directory (default: /harness)
- `show_diff` - Show git diff after execution (default: false)
- `react_upgrade` - Enable React upgrade mode (default: true)

## Troubleshooting

### Common Issues

**PR Not Created**
- Verify `harnessKey` has permissions to create PRs in your project
- Check that the source and target branches are different
- Ensure `REPO_NAME` is correctly set

**No Changes Detected**
- The coding agent may not have made any modifications
- Review the prompt for clarity and specificity
- Check the coding agent logs for errors

**Branch Already Exists**
- The agent automatically adds a timestamp suffix to create a unique branch
- Old branches can be deleted manually if no longer needed

**API Connection Issues**
- Verify the `anthropicKey` is valid and has quota remaining
- Check network connectivity from the Harness delegate

### Best Practices

1. **Write Clear Prompts**: Be specific about what changes you want
2. **Review PRs Carefully**: Always review AI-generated changes before merging
3. **Run Tests**: Ensure your test suite passes after changes
4. **Incremental Changes**: Break large upgrades into smaller, manageable prompts
5. **Version Control**: Keep your prompts in version control for reproducibility

## Advanced Usage

### Chaining Multiple Prompts

You can run multiple agent executions in sequence:
```yaml
steps:
  - name: upgrade_react
    # Prompt: "Upgrade React to version 18"
  - name: fix_types
    # Prompt: "Fix all TypeScript type errors"
  - name: optimize
    # Prompt: "Add performance optimizations"
```

### Custom Branch Names

While the base branch name is fixed, you can modify the pipeline to use different branch patterns by editing the `push_to_branch` step.

## Support

For issues or questions:
- Check the pipeline execution logs
- Review the coding agent output for AI reasoning
- Verify all required inputs are provided
- Ensure git connector has proper permissions
