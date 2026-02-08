FROM mcr.microsoft.com/devcontainers/python:3.13-trixie

# Install uv (Python package manager) - required for specify CLI
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv bin path is available
ENV PATH="/home/vscode/.local/bin:${PATH}"

# Install specify CLI from spec-kit repository
RUN uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Install GitHub Copilot CLI
RUN npm install -g @github/copilot@latest
