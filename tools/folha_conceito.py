"""Monta a folha de conceito: as vistas (PNG com fundo transparente) lado a lado, na mesma
altura, sobre cinza liso #808080.

Uso: python3 tools/folha_conceito.py <saida.png> <vista.png> [<vista.png> ...]
Precisa do Pillow. As vistas vêm de renders ortográficos com a mesma escala, então a altura
do personagem bate entre elas sem redimensionar.
"""
import sys

from PIL import Image

CINZA = (128, 128, 128, 255)


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    vistas = [Image.open(c).convert("RGBA") for c in sys.argv[2:]]
    altura = max(v.height for v in vistas)
    folha = Image.new("RGBA", (sum(v.width for v in vistas), altura), CINZA)
    x = 0
    for v in vistas:
        folha.alpha_composite(v, (x, altura - v.height))
        x += v.width
    folha.convert("RGB").save(sys.argv[1], optimize=True)
    print(f"{sys.argv[1]}: {folha.width}x{folha.height}")


if __name__ == "__main__":
    main()
