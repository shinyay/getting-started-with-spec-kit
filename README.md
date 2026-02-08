# Getting Started with Spec Kit

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shinyay/getting-started-with-spec-kit)

A ready-to-use Dev Container for experiencing [GitHub Spec Kit](https://github.com/github/spec-kit) — zero installation required.

## What is Spec Kit?

Spec Kit is an open source toolkit for **Spec-Driven Development (SDD)**. It helps you focus on product scenarios and predictable outcomes instead of vibe coding every piece from scratch.

## Quick Start

### Option 1: GitHub Codespaces (Recommended)

Click the **"Open in GitHub Codespaces"** badge above to launch a fully configured environment in your browser.

### Option 2: VS Code + Dev Containers

1. Install [Docker](https://www.docker.com/products/docker-desktop) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Clone this repository
3. Open in VS Code and click **"Reopen in Container"** when prompted

### After the Container Starts

The `specify` CLI is pre-installed. Start using Spec Kit immediately:

```bash
# Initialize Spec Kit in this directory
specify init . --ai copilot

# Verify all tools are configured
specify check
```

Then follow the Spec-Driven Development workflow:

```bash
/speckit.constitution    # Establish project principles
/speckit.specify         # Define what you want to build
/speckit.plan            # Create technical implementation plan
/speckit.tasks           # Break down into actionable tasks
/speckit.implement       # Execute implementation
```

## What's Included

| Tool | Purpose |
|------|---------|
| Python 3.13 | Runtime for Spec Kit |
| uv | Python package manager |
| specify CLI | Spec Kit's CLI tool |
| Node.js LTS | Runtime for AI agent CLIs |
| GitHub Copilot CLI | AI coding assistant |
| Git (latest) | Version control |

## References

- [Spec Kit Repository](https://github.com/github/spec-kit)
- [Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Dev Containers Specification](https://containers.dev/)

## Licence

Released under the [MIT license](https://gist.githubusercontent.com/shinyay/56e54ee4c0e22db8211e05e70a63247e/raw/f3ac65a05ed8c8ea70b653875ccac0c6dbc10ba1/LICENSE)

## Author

- github: <https://github.com/shinyay>
- twitter: <https://twitter.com/yanashin18618>
- mastodon: <https://mastodon.social/@yanashin>
