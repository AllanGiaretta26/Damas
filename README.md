# Jogo de Damas em Python

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-tkinter-informational)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Licença](https://img.shields.io/badge/licença-MIT-lightgrey)

> Jogo de damas completo com interface gráfica em tkinter, IA baseada em minimax com poda alfa-beta e arquitetura orientada a princípios SOLID.

---

## Descrição

Implementação do jogo de damas com todas as regras tradicionais: capturas obrigatórias, múltiplas capturas em sequência, promoção de peças a dama e desfazer jogada. O projeto oferece dois modos — duelo humano vs. humano ou partida contra uma IA com três níveis de dificuldade, incluindo minimax com poda alfa-beta nos níveis Médio e Difícil.

A arquitetura segue princípios SOLID com separação clara de responsabilidades entre modelos, serviços, IA e interface gráfica.

---

## Status do Projeto

![Status](https://img.shields.io/badge/status-concluído-brightgreen)

Projeto concluído e funcional.

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Tkinter](https://img.shields.io/badge/tkinter-GUI-informational)

- **Python 3.7+** — linguagem principal
- **tkinter** — interface gráfica (incluso na instalação padrão do Python)
- Sem dependências externas

---

## Como Instalar e Rodar

### Pré-requisitos

- Python 3.7 ou superior
- tkinter (já incluso na maioria das instalações do Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/AllanGiaretta26/Damas.git
cd Damas

# Execute o jogo
python main.py
```

No Windows, o script alternativo também funciona:

```bat
scripts\executar_jogo.bat
```

### Executar Testes

```bash
python tests/teste_jogo.py
```

---

## Como Jogar

1. Execute `python main.py`
2. Escolha o modo de jogo:
   - **Dois Jogadores** — humano vs. humano
   - **Contra a IA** — escolha a dificuldade (Fácil / Médio / Difícil) e sua cor (Vermelho ou Azul)
3. Clique em uma de suas peças para selecioná-la
4. Clique em uma casa destacada para mover:
   - Verde = movimento simples
   - Laranja = captura
5. Capturas são obrigatórias quando disponíveis
6. Use o botão **Desfazer** para reverter a última jogada (modo IA)
7. Use o botão **Empate** para encerrar a partida sem vencedor
8. Use o botão **Menu** para voltar ao menu inicial sem fechar o app

**Cores:** Vermelho = Jogador 1 | Azul = Jogador 2 / IA | Coroa = dama promovida

---

## IA — Níveis de Dificuldade

| Nível | Estratégia | Tempo médio por jogada |
|---|---|---|
| Fácil | Movimentos aleatórios | < 1 ms |
| Médio | Minimax com poda alfa-beta (profundidade 3) | ~50–200 ms |
| Difícil | Minimax com poda alfa-beta (profundidade 5) | ~0.1–3 s |

A função de avaliação considera material (peça comum = 1 ponto, dama = 3) e posição: bônus de centralização e bônus de proteção para peças na linha de fundo. Movimentos de captura são explorados primeiro para melhorar a eficiência da poda.

---

## Estrutura do Projeto

```
Damas/
├── main.py                          # Ponto de entrada e menu inicial
├── src/
│   ├── config.py                    # Configurações globais (cores, tamanhos)
│   ├── game.py                      # Orquestrador do jogo (Jogo)
│   ├── models/                      # Estado puro: Tabuleiro, Peca, enums
│   ├── services/                    # Regras: validação, capturas, promoção
│   ├── ia/                          # IA: factory + estratégias minimax
│   └── gui/                         # Interface tkinter: renderização e eventos
├── tests/
│   └── teste_jogo.py
└── scripts/
    └── executar_jogo.bat
```

---

## Exemplos de Uso Programático

```python
from src.game import Jogo

jogo = Jogo()
jogo.selecionar_peca(2, 1)
print(jogo.movimentos_validos)
jogo.mover_peca(2, 1, 3, 0)

jogo.desfazer_jogada()

fim, vencedor = jogo.verificar_fim_de_jogo()
if fim:
    print(f"Vencedor: {vencedor}")
```

---

## Solução de Problemas

**`ModuleNotFoundError: No module named 'tkinter'`**

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS
brew install python-tk
```

---

## Licença

Este projeto está sob a licença [MIT](./LICENSE).

---

Desenvolvido por [Allan Giaretta](https://github.com/AllanGiaretta26).
