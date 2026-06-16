# Damas ♟️

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![tkinter](https://img.shields.io/badge/GUI-tkinter-lightgrey)
![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)
![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

> Jogo de damas desktop com interface gráfica, modo humano vs. humano e IA com três níveis de dificuldade — incluindo minimax com poda alfa-beta.

---

## Descrição

Aplicação desktop de damas construída em Python puro com tkinter. O projeto implementa as regras completas do jogo — captura obrigatória, sequência de capturas, promoção a dama — e oferece um adversário controlado por IA capaz de planejar jogadas vários turnos à frente.

O código é organizado em camadas (modelos, serviços, IA, GUI) e acompanha uma suíte de testes procedurais que cobre os principais cenários do jogo.

## Tecnologias

- **Python 3.7+**
- **tkinter** — interface gráfica nativa, sem dependências externas
- **Minimax com poda alfa-beta** — motor de IA

## Como Instalar e Rodar

**Pré-requisitos:** Python 3.7 ou superior com tkinter disponível.

```bash
git clone https://github.com/AllanGiaretta26/Damas.git
cd Damas
python main.py
```

No Windows, há um atalho pronto:

```bat
scripts\executar_jogo.bat
```

> `requirements.txt` é apenas informativo — o projeto não tem dependências de runtime além da biblioteca padrão.

### Problema com tkinter?

Se aparecer `ModuleNotFoundError: No module named 'tkinter'`, instale o pacote para sua plataforma:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (Homebrew)
brew install python-tk
```

No Windows, reinstale o Python marcando a opção **Tcl/Tk** no instalador oficial.

## Testes

A suíte usa `assert` direto — sem pytest nem unittest. Cobre inicialização, movimentos simples, capturas, capturas obrigatórias, sequências, promoção, dama, fim de jogo, histórico e desfazer.

```bash
python tests/teste_jogo.py
```

Para executar um teste isolado:

```bash
python -c "from tests.teste_jogo import teste_desfazer_captura; teste_desfazer_captura()"
```

## Como Jogar

1. Execute `python main.py` e escolha o modo:
   - **Dois Jogadores** — humano vs. humano na mesma máquina
   - **Contra a IA** — escolha a dificuldade e sua cor
2. Clique em uma peça do jogador atual para selecioná-la.
3. Clique em uma casa destacada para mover ou capturar.
4. **Captura é obrigatória** — se existir captura disponível, só ela será permitida.
5. Se uma captura abrir nova captura pela mesma peça, o turno continua até encerrar a sequência.
6. Use os botões da barra inferior: `Novo Jogo`, `Empate`, `Desfazer` (modo IA), `Histórico`, `Menu` e `Sair`.

**Cores e posições iniciais:**

| Jogador | Cor | Linhas iniciais | Promove em |
|---|---|---|---|
| Jogador 1 | Vermelho | 5–7 (move para cima) | Linha 0 |
| Jogador 2 / IA | Azul | 0–2 (move para baixo) | Linha 7 |

## IA

| Dificuldade | Estratégia |
|---|---|
| Fácil | Movimento aleatório |
| Médio | Minimax com poda alfa-beta, profundidade 3 |
| Difícil | Minimax com poda alfa-beta, profundidade 5 |

A IA pode jogar com qualquer cor — no menu, escolha a cor do humano e a IA assumirá a oposta.

## Estrutura do Projeto

```text
Damas/
├── main.py                  # Janela única, menu, opções de IA e agendamento da IA
├── src/
│   ├── config.py            # Constantes visuais e temas
│   ├── game.py              # Orquestrador de estado e regras públicas
│   ├── models/              # Peca, Tabuleiro e enums
│   ├── services/            # Validação, captura e promoção
│   ├── ia/                  # Factory de IA e estratégias
│   └── gui/                 # Renderização e eventos tkinter
├── tests/
│   └── teste_jogo.py        # Testes procedurais
├── scripts/
│   └── executar_jogo.bat
└── docs/                    # Documentação técnica
```

## Documentação

- [Índice](docs/README.md)
- [Arquitetura](docs/arquitetura/visao-geral.md)
- [Referência técnica](docs/referencia/README.md)
- [Guias práticos](docs/guias/README.md)
- [Auditorias](docs/auditorias/README.md)

## Licença

Este projeto está sob a licença [MIT](./LICENSE).

---
Desenvolvido por [Allan Giaretta](https://github.com/allangiaretta26).
