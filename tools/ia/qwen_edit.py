"""Edita uma imagem de referência no Space Qwen-Image-Edit pela API do Gradio.

Uso: tools/ia.sh qwen_edit.py <prompt.md> <bloco> <imagem> <pasta_saida> <nome> <seed> [<seed> ...]

Lê o bloco ``` de número <bloco> (1 = primeiro) de <prompt.md> como prompt,
manda <imagem> como entrada, com a reescrita de prompt desligada, e grava uma
imagem por seed em <pasta_saida>/<nome>-<seed>.<ext>. Imprime uma linha por imagem.
"""
import re
import shutil
import sys
from pathlib import Path

from gradio_client import Client, handle_file

SPACE = "Qwen/Qwen-Image-Edit"


def ler_prompt(caminho: Path, bloco: int) -> str:
    blocos = re.findall(r"```\n(.*?)\n```", caminho.read_text(encoding="utf-8"), re.S)
    if not 1 <= bloco <= len(blocos):
        sys.exit(f"{caminho} tem {len(blocos)} blocos ```, pedi o {bloco}")
    return " ".join(blocos[bloco - 1].split())


def main() -> None:
    if len(sys.argv) < 7:
        sys.exit(__doc__)
    prompt = ler_prompt(Path(sys.argv[1]), int(sys.argv[2]))
    imagem = Path(sys.argv[3])
    saida = Path(sys.argv[4])
    nome = sys.argv[5]
    saida.mkdir(parents=True, exist_ok=True)
    cliente = Client(SPACE, verbose=False)
    for seed in (int(s) for s in sys.argv[6:]):
        resultado, usada = cliente.predict(
            image=handle_file(str(imagem)), prompt=prompt, seed=seed,
            randomize_seed=False, true_guidance_scale=4.0,
            num_inference_steps=50, rewrite_prompt=False, api_name="/infer",
        )
        origem = Path(resultado if isinstance(resultado, str) else resultado["path"])
        destino = saida / f"{nome}-{int(usada)}{origem.suffix}"
        shutil.copyfile(origem, destino)
        print(f"Qwen seed={int(usada)} -> {destino}", flush=True)


if __name__ == "__main__":
    main()
