# Getting Started with Spec Kit

> **Stop vibe coding. Start specifying.**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shinyay/getting-started-with-spec-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://gist.githubusercontent.com/shinyay/56e54ee4c0e22db8211e05e70a63247e/raw/f3ac65a05ed8c8ea70b653875ccac0c6dbc10ba1/LICENSE)

A hands-on workshop for [GitHub Spec Kit](https://github.com/github/spec-kit) — **18 scenarios** across 4 difficulty levels that teach you Spec-Driven Development by building real software. Zero installation required.

## 💡 What is Spec-Driven Development?

You prompt an AI, get unpredictable code, and spend hours fixing what it guessed wrong.

**Spec-Driven Development (SDD)** flips that. You write a structured specification *first*, then the AI follows it — producing predictable, high-quality output every time.

```
1. Constitution   Define project principles and constraints
2. Specify        Describe what you want to build
3. Clarify        Surface hidden assumptions         ← this is where SDD pays off
4. Plan           Choose architecture and technology
5. Tasks          Break down into executable steps
6. Implement      Generate code from specifications
```

The **Clarify** step is where SDD pays off: Spec Kit surfaces the hidden assumptions and edge cases you didn't think about — *before* a single line of code is written.

## 🚀 Quick Start

**Prerequisites:** A GitHub account with [GitHub Copilot](https://github.com/features/copilot) access.

### 1. Launch the environment

Click the **"Open in GitHub Codespaces"** badge above — you'll have a fully configured environment in ~60 seconds.

<details>
<summary>Alternative: VS Code + Dev Containers (local)</summary>

1. Install [Docker](https://www.docker.com/products/docker-desktop) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Clone this repository
3. Open in VS Code → click **"Reopen in Container"** when prompted

</details>

### 2. Initialize Spec Kit

```bash
specify init . --ai copilot
specify check
```

### 3. Pick a scenario and go

Open a scenario file from the table below, then follow the phase prompts — each one is a `/speckit.*` command you run in **Copilot Chat** (not the terminal):

```
/speckit.constitution    Define project principles and constraints
/speckit.specify         Describe what you want to build
/speckit.clarify         Surface hidden assumptions and edge cases
/speckit.plan            Choose architecture and technology
/speckit.tasks           Break down into executable steps
/speckit.implement       Generate code from specifications
```

## 🎓 Workshop Scenarios

**18 hands-on scenarios** — from beginner CRUD apps to distributed systems.

| Level | Scenarios | What You'll Specify |
|---|---|---|
| ⭐ Beginner | A · J · K · L | SDD workflow, data modeling, state machines, calculation correctness |
| ⭐⭐ Intermediate | H · M · N · O | API contracts, HTTP semantics, ordering algorithms, data validation |
| ⭐⭐⭐ Intermediate–Advanced | B · C · D · G · I | Offline sync, auth flows, billing, IaC governance, API versioning |
| ⭐⭐⭐⭐ Advanced | E · F · P · Q · R | Real-time concurrency, pipelines, sagas, plugin platforms, experimentation |

> [!TIP]
> **First time?** Start with **[Scenario A — QuickRetro](scenarios/A-quick-retro.md)**. It's the simplest domain and teaches the full SDD workflow in ~90 minutes.

👉 **[Browse all scenarios with detailed guides →](SCENARIOS.md)**

## 🛠️ What's Inside

This Dev Container comes pre-configured and ready to go:

- **Python 3.13 + uv** — Runtime and package manager for Spec Kit
- **`specify` CLI** — Spec Kit's command-line tool, pre-installed
- **Node.js LTS** — Runtime for AI agent tooling
- **GitHub Copilot + Copilot Chat** — AI coding assistant (VS Code extensions included)
- **Git + GitLens + Git Graph** — Version control with visual history

No setup. No configuration. Just open and start specifying.

## 📚 Learn More

- [**Spec Kit**](https://github.com/github/spec-kit) — The open-source SDD toolkit
- [**Spec-Driven Development Methodology**](https://github.com/github/spec-kit/blob/main/spec-driven.md) — The full SDD methodology guide
- [**Workshop Guide**](WORKSHOP.md) — Facilitator guide with timing, teaching tips, and baseline contracts
- [**Dev Containers Specification**](https://containers.dev/) — How Dev Containers work

## 🤝 Feedback

Found a bug? Have an idea for a new scenario? [Open an issue](https://github.com/shinyay/getting-started-with-spec-kit/issues/new) — contributions and suggestions are welcome.

## License

Released under the [MIT License](https://gist.githubusercontent.com/shinyay/56e54ee4c0e22db8211e05e70a63247e/raw/f3ac65a05ed8c8ea70b653875ccac0c6dbc10ba1/LICENSE).

## Author

**[@shinyay](https://github.com/shinyay)** · [Twitter](https://twitter.com/yanashin18618) · [Mastodon](https://mastodon.social/@yanashin)

---

<p align="center">
  <em>Presenting this workshop at an event? Share this QR code with attendees:</em><br><br>
  <img src="QR.png" alt="QR code to this repository" width="180">
</p>
