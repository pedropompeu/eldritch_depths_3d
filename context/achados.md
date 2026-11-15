---
tipo: contexto
projeto: eldritch-depths-3d
descricao: Bugs, riscos e dívidas do Eldritch Depths 3D, com severidade, local, reprodução e fix.
estado: estavel
criado: 2026-11-14
relacionado:
  - context/arquitetura.md
---

# Achados

> Ler **antes de dizer que algo está pronto** ou de mexer em área crítica. Todo achado leva severidade (justificada pela consequência), onde, reprodução e fix. Achado resolvido não se apaga: ganha uma linha `Resolvido` com data.

## A01 · Verificação de autoload que sempre falha desliga integrações sem aviso {#has-singleton}

- [2026-11-14] (e) **Severidade:** alto — bônus de perks, saves disparados por perks e outras integrações ficam desligados em silêncio, e o jogador nunca recebe o que o jogo promete.
- [2026-11-14] (e) **Onde:** projeto 2D, 59 ocorrências de `Engine.has_singleton("<Autoload>")`; por exemplo `scripts/components/stats_component.gd:91` (`PerksManager`). Afeta todo código portado.
- [2026-11-14] (e) **Reprodução:** com a Godot 4.7.2, um script `--headless` que imprime `Engine.has_singleton("SaveManager")` dá `false` enquanto o nó `/root/SaveManager` existe.
- [2026-11-14] (i) **Fix:** no 3D, usar `Autoloads.get_autoload(&"Nome")` (T05 do plano) e checar `has_method` antes de chamar. `grep -rn has_singleton scripts/` deve voltar vazio.

## A02 · A arte pode não chegar ao nível da Steam e do portfólio {#risco-arte}

- [2026-11-14] (i) **Severidade:** alto — arte feia é anti-meta declarada por Pedro; se o pipeline falhar, o jogo funciona mas não serve a nenhum dos dois usos.
- [2026-11-14] (e) **Onde:** trilha de arte (Bloco 1B, plano próprio a escrever).
- [2026-11-14] (e) **Reprodução:** não é bug; vem das restrições — modelos 3D originais, Pedro nunca usou Blender, geração 3D por IA local exige NVIDIA (ausente nesta máquina), orçamento R$ 0.
- [2026-11-14] (i) **Fix / mitigação:** guia de estilo antes da produção em série; conceito do Cavaleiro aprovado por Pedro antes de modelar; prova do pipeline IA → Blender → Godot com uma peça pequena; pré-visualizações renderizadas a cada etapa. A trilha de jogo segue com provisórios para não esperar a arte.

## A03 · Teste que quebrava passava como aprovado {#runner-silencioso}

- [2026-11-14] (e) **Severidade:** alto — com vários modelos escrevendo testes, um teste com erro de script contava como aprovado e um script com erro de sintaxe travava a suíte para sempre; o `OK` deixava de significar alguma coisa.
- [2026-11-14] (e) **Onde:** `tests/run_tests.gd` (versão do commit `85efc13`, T02).
- [2026-11-14] (e) **Reprodução:** um `test_*.gd` com `var n = null; n.metodo()` dava `OK: 6 testes`; um com `func test_x(:` travava o runner (o `load` devolve o script, o `new()` falha e a função do runner aborta sem chamar `quit`).
- [2026-11-14] (i) **Fix:** `Logger` que converte erro da engine em falha, checagem `can_instantiate()` e vigia de 30 s por teste. Resolvido em 2026-11-14 — conferido com quatro testes temporários (erro de script, `push_error`, sintaxe, `await` eterno), todos reprovados; `push_warning` passou.
