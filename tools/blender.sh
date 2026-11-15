#!/usr/bin/env bash
# Roda um script Python no Blender sem janela, a partir da raiz do repositório.
# Uso: tools/blender.sh <script.py> [args...]  (os args chegam ao script depois de "--")
set -u
cd "$(dirname "$0")/.."
script="$1"; shift
exec "${BLENDER:-blender}" -b --factory-startup --python-exit-code 1 --python "$script" -- "$@"
