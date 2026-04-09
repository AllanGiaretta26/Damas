# Organização do Projeto

**Data:** 09/04/2026 15:00
**Tipo:** refatoracao
**Autor:** Agente IA

## Descrição

Reorganização completa da estrutura de arquivos e diretórios do projeto Jogo de Damas para seguir melhores práticas de organização de projetos Python.

## Motivação

O projeto tinha:
- Documentação espalhada na raiz (7+ arquivos `.md`)
- Scripts de execução na raiz (`executar_jogo.bat`, `executar_jogo.sh`)
- Arquivo de testes na raiz (`teste_jogo.py`)
- Arquivos temporários (`.qwen/settings.json.orig`, `__pycache__/`)
- Sem separação clara entre código fonte, testes, scripts e documentação

## Detalhes Técnicos

### Estrutura Criada

```
IA-VScode/
├── main.py                 # Ponto de entrada (único arquivo na raiz além de README e config)
├── README.md               # Documentação principal
├── requirements.txt        # Dependências
├── .gitignore             # Configuração do git
│
├── src/                   # Código fonte principal
│   ├── models/            # Classes de domínio
│   ├── services/          # Serviços especializados
│   ├── ia/                # Inteligência Artificial
│   ├── gui/               # Interface Gráfica
│   ├── game.py            # Orquestrador do jogo
│   └── config.py          # Configurações
│
├── tests/                 # Testes automatizados
│   ├── __init__.py
│   └── teste_jogo.py
│
├── scripts/               # Scripts utilitários e exemplos
│   ├── executar_jogo.bat
│   ├── executar_jogo.sh
│   └── exemplos_avancados.py
│
└── docs/                  # Documentação completa
    ├── INDEX.md           # Índice
    ├── guides/            # Guias de início rápido
    └── ...                # Demais documentos
```

### Princípios Aplicados

1. **Separação de Preocupações**: Cada diretório tem propósito claro
2. **Raiz Limpa**: Apenas arquivos essenciais para iniciar o projeto
3. **Nomenclatura Padrão**: `tests/`, `scripts/`, `docs/` seguindo convenções Python
4. **Documentação Centralizada**: Toda documentação em `docs/` com índice

## Impactos

- **Módulos afetados**: Nenhum (apenas reorganização de arquivos)
- **Possíveis breaking changes**: Nenhum (código fonte inalterado)

## Decisões Tomadas

### 1. Manter `main.py` na raiz
**Decisão**: Ponto de entrada permanece na raiz para facilitar execução

**Racional**: Padrão Python comum, fácil encontrar e executar

### 2. Tests em `tests/` ao invés de `test/`
**Decisão**: Usar plural seguindo convenção de muitos projetos Python

**Racional**: Mais comum em projetos open source Python

### 3. Scripts em `scripts/` ao invés de `bin/`
**Decisão**: Nome mais descritivo para scripts utilitários

**Racional**: `scripts/` é mais claro para quem não está familiarizado com convenção Unix

## Próximos Passos

- [ ] Adicionar Makefile ou pyproject.toml para comandos padronizados
- [ ] Configurar CI/CD com GitHub Actions
- [ ] Adicionar pré-commit hooks para formatação automática
