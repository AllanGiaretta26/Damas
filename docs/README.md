# Documentação do projeto

Esta pasta contém apenas índices e subpastas. Documentação temática solta na raiz de `docs/` vira bagunça; por isso os documentos foram agrupados por papel.

## Ordem de autoridade

Use esta ordem quando houver conflito entre documentos:

1. Código e testes.
2. `CLAUDE.md`, por registrar regras operacionais do repositório.
3. Documentação técnica em `docs/`.
4. `README.md`, como guia de entrada para uso e execução.
5. Relatórios em `docs/auditorias/`, como histórico de auditoria.

## Estrutura

| Pasta | Papel |
|---|---|
| [arquitetura/](arquitetura/) | Explicação da arquitetura e invariantes do domínio. |
| [referencia/](referencia/) | Referência técnica de módulos, classes e contratos. |
| [guias/](guias/) | Exemplos executáveis, cuidados e checklists de manutenção. |
| [auditorias/](auditorias/) | Auditorias e histórico de refatoração documental. |

## Entrada recomendada

1. [Arquitetura](arquitetura/visao-geral.md)
2. [Referência técnica](referencia/README.md)
3. [Exemplos de uso](guias/uso-exemplo.md)
4. [Pontos de atenção](guias/pontos-atencao.md)

## Regras de manutenção

- Não adicione arquivos temáticos diretamente em `docs/`; crie ou use uma subpasta.
- Preserve `docs/README.md` apenas como índice e política de documentação.
- Não documente comportamento planejado como se existisse.
- Preserve nomes de métodos, labels e chaves exatamente como aparecem no código quando forem literais.
- Use português brasileiro para texto explicativo.
- Evite copiar blocos grandes de implementação. Documente contratos, invariantes e pontos de extensão.
- Ao mudar regras de jogo, atualize `docs/referencia/services.md`, `docs/referencia/game.md`, `docs/guias/pontos-atencao.md` e os testes.
- Ao mudar interface ou labels, atualize `README.md`, `docs/referencia/gui.md` e `docs/referencia/main.md`.

## Verificação recomendada

```bash
python tests/teste_jogo.py
git diff --check
```

Também valide links relativos e H1 único por documento antes de entregar mudanças de documentação.
