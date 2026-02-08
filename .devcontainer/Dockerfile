FROM mcr.microsoft.com/devcontainers/python:3.13-trixie

# Install uv system-wide from official image (avoids curl-to-root PATH issues)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Switch to vscode user for user-scoped tool installation
USER vscode

# Install specify CLI (installs to ~/.local/bin/)
RUN uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
ENV PATH="/home/vscode/.local/bin:${PATH}"

# Switch back to root so devcontainer features can install properly
USER root
