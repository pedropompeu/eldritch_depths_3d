#!/usr/bin/env bash
# Roda um script de tools/ia/ no ambiente isolado com o gradio_client.
# Primeira vez: python3 -m venv tools/ia/.venv && tools/ia/.venv/bin/pip install gradio_client
set -euo pipefail
raiz="$(cd "$(dirname "$0")/.." && pwd)"
script="$1"; shift
exec "$raiz/tools/ia/.venv/bin/python" "$raiz/tools/ia/$script" "$@"
