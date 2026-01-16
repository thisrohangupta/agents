# Feature Flag Cleanup

## Overview

The **Feature Flag Cleanup** is an agent designed to automatically search stale feature flags in your code and remove it within your Continuous Integration (CI) pipelines. When a pipeline runs, the agent analyzes code behind a stale feature flag and its current treatment to applies safe and scoped refactor, and raises pull requests (PRs) with clear explanations.

The goal is to optimize developers' work, keep the codebase clean, and automate the cleanup of stale feature flags through the pipeline.

---

## Key Capabilities

- 🔁 **Pull Request Automation**

  - Creates PRs with human-readable explanations
  - Links fixes back to CI failures and root cause
  - Re-runs CI to validate fixes before marking ready
