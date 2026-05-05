#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="$ROOT/.local/bin"
MAMBA_ROOT="$ROOT/.micromamba"
MICROMAMBA="$BIN_DIR/micromamba"

mkdir -p "$BIN_DIR" "$MAMBA_ROOT" "$ROOT/logs"

if [[ ! -x "$MICROMAMBA" ]]; then
  echo "Installing micromamba into $MICROMAMBA"
  case "$(uname -m)" in
    arm64|aarch64) ARCH="osx-arm64" ;;
    x86_64) ARCH="osx-64" ;;
    *) echo "Unsupported architecture: $(uname -m)" >&2; exit 2 ;;
  esac
  curl -Ls "https://micro.mamba.pm/api/micromamba/${ARCH}/latest" -o "$ROOT/.local/micromamba.tar.bz2"
  tar -xjf "$ROOT/.local/micromamba.tar.bz2" -C "$ROOT/.local" bin/micromamba
fi

ENV_FILE="${1:-$ROOT/environment-core.yml}"
export MAMBA_ROOT_PREFIX="$MAMBA_ROOT"
"$MICROMAMBA" env create -y -f "$ENV_FILE" 2>&1 | tee "$ROOT/logs/micromamba_env_create.log"

echo
echo "Environment created. Activate with:"
echo "  export MAMBA_ROOT_PREFIX=\"$MAMBA_ROOT\""
echo "  eval \"\$($MICROMAMBA shell hook -s zsh)\""
echo "  micromamba activate $(grep '^name:' "$ENV_FILE" | awk '{print $2}')"
echo
echo "Or run commands without activation:"
echo "  $MICROMAMBA run -n $(grep '^name:' "$ENV_FILE" | awk '{print $2}') make status"
