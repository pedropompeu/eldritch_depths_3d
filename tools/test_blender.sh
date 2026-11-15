#!/usr/bin/env bash
# Roda os testes do kit do Blender. Última linha: "OK: <n> testes" (código 0) ou "FALHOU: <x> de <n>" (código 1).
set -u
cd "$(dirname "$0")/.."
saida=$(tools/blender.sh tools/blender/tests/test_ed_blender.py 2>&1)
rc=$?
printf '%s\n' "$saida" | grep -v '^Blender quit$' | grep -v '^$'
[ "$rc" -eq 0 ] || exit 1
printf '%s\n' "$saida" | grep -q '^OK: [0-9]* testes$' || exit 1
