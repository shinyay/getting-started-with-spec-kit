#!/bin/bash
set -uo pipefail

echo ""
echo "🔍 Setting up Spec Kit Dev Container..."
echo ""

# Upgrade specify CLI to the latest version
echo "⬆️  Upgrading specify CLI to latest..."
if uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git 2>&1 | tail -1; then
    echo "✅ specify CLI is up to date"
else
    echo "⚠️  specify CLI upgrade failed (using version baked into image)"
fi

# Verify tools
echo ""
echo "🔧 Installed tools:"

if command -v specify &> /dev/null; then
    echo "  ✅ specify CLI"
else
    echo "  ❌ specify CLI - NOT FOUND"
fi

if command -v uv &> /dev/null; then
    echo "  ✅ uv $(uv --version 2>/dev/null | head -1)"
else
    echo "  ❌ uv - NOT FOUND"
fi

if command -v git &> /dev/null; then
    echo "  ✅ git $(git --version 2>/dev/null | sed 's/git version //')"
else
    echo "  ❌ git - NOT FOUND"
fi

if command -v python &> /dev/null; then
    echo "  ✅ python $(python --version 2>/dev/null | sed 's/Python //')"
else
    echo "  ❌ python - NOT FOUND"
fi

if command -v node &> /dev/null; then
    echo "  ✅ node $(node --version 2>/dev/null)"
else
    echo "  ❌ node - NOT FOUND"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌱 Spec Kit Dev Container is ready!"
echo ""
echo "Quick Start:"
echo "  1. specify init . --ai copilot     # Initialize Spec Kit here"
echo "  2. specify check                    # Verify all tools"
echo ""
echo "More info: https://github.com/github/spec-kit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
