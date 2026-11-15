#!/usr/bin/env bash
# Mede o fps da cena principal no modo automático (herói jogando sozinho).
# Uso: tools/measure_fps.sh <mobile|gl_compatibility>
# Saída: "renderer=<r> media=<x> minimo=<y>", descartando os primeiros 5 s.
set -u
r="${1:-}"
case "$r" in
	mobile|gl_compatibility) ;;
	*) echo "uso: $0 <mobile|gl_compatibility>" >&2; exit 2 ;;
esac
cd "$(dirname "$0")/.."
GODOT="${GODOT:-godot}"
# O Godot imprime "Project FPS: N (x mspf)" uma vez por segundo.
"$GODOT" --path . --rendering-method "$r" --resolution 1920x1080 --print-fps --quit-after 1800 -- --autoplay 2>&1 \
	| awk -v r="$r" '
		/Project FPS:/ {
			n++
			if (n <= 5) next
			v = $3 + 0
			soma += v
			c++
			if (c == 1 || v < minimo) minimo = v
		}
		END {
			if (c == 0) { print "renderer=" r " sem amostras depois de 5 s" > "/dev/stderr"; exit 1 }
			printf "renderer=%s media=%.1f minimo=%d\n", r, soma / c, minimo
		}'
