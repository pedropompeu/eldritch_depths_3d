"""Gera imagens no Space FLUX.1 [schnell] pela API do Gradio.

Uso: tools/ia.sh flux.py <prompt.md> <pasta_saida> <seed> [<seed> ...]

Lê o primeiro bloco ``` de <prompt.md> como prompt e grava uma imagem por
seed em <pasta_saida>/flux-<seed>.<ext>. Imprime uma linha por imagem.
"""
import re
import shutil
import sys
from pathlib import Path

from gradio_client import Client

SPACE = "black-forest-labs/FLUX.1-schnell"


def ler_prompt(caminho: Path) -> str:
    m = re.search(r"```\n(.*?)\n```", caminho.read_text(encoding="utf-8"), re.S)
    if not m:
        sys.exit(f"sem bloco ``` em {caminho}")
    return " ".join(m.group(1).split())


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    prompt = ler_prompt(Path(sys.argv[1]))
    saida = Path(sys.argv[2])
    saida.mkdir(parents=True, exist_ok=True)
    cliente = Client(SPACE, verbose=False)
    for seed in (int(s) for s in sys.argv[3:]):
        imagem, usada = cliente.predict(
            prompt=prompt, seed=seed, randomize_seed=False,
            width=1024, height=1024, num_inference_steps=4, api_name="/infer",
        )
        origem = Path(imagem if isinstance(imagem, str) else imagem["path"])
        destino = saida / f"flux-{int(usada)}{origem.suffix}"
        shutil.copyfile(origem, destino)
        print(f"FLUX seed={int(usada)} -> {destino}", flush=True)


if __name__ == "__main__":
    main()
