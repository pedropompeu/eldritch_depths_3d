#!/usr/bin/env bash
# Roda todos os testes do projeto. Última linha de sucesso: "OK: <n> testes", código 0.
set -u
cd "$(dirname "$0")/.."
GODOT="${GODOT:-godot}"
# Importa primeiro para registrar class_name novos no cache global de classes.
"$GODOT" --headless --path . --import >/dev/null 2>&1
# O runner tem vigia por teste; o timeout geral é só a última rede de proteção.
timeout 900 "$GODOT" --headless --path . -s res://tests/run_tests.gd
