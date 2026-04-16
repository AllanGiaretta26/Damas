# Jogo de Damas em Python

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-tkinter-informational)
![Licença](https://img.shields.io/badge/licença-MIT-lightgrey)

> Jogo de damas completo com interface gráfica em tkinter, modo contra IA e arquitetura baseada em princípios SOLID e Clean Code.

---

## Descrição

Implementação do jogo de damas com todas as regras tradicionais, incluindo capturas obrigatórias, múltiplas capturas em sequência e promoção de peças a dama. O projeto oferece dois modos: duelo entre dois jogadores humanos ou partida contra uma IA baseada em heurísticas de priorização.

A arquitetura segue princípios SOLID com separação clara de responsabilidades entre modelos, serviços, IA e interface gráfica.

---

## Status do Projeto

![Status](https://img.shields.io/badge/status-concluído-brightgreen)

Projeto concluído e funcional. Melhorias futuras listadas ao final deste documento.

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

- Python 3.7 ou superior instalado
- tkinter (já incluso no Python na maioria dos sistemas)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/AllanGiaretta26/Damas.git
cd Damas

# Execute o jogo
python main.py
```

Alternativamente, use os scripts prontos:

```bash
# Windows
scripts/executar_jogo.bat

# Linux / macOS
bash scripts/executar_jogo.sh
```

### Executar Testes

```bash
python tests/teste_jogo.py
```

---

## Como Jogar

1. Execute `python main.py`
2. Escolha o modo: **Dois Jogadores** ou **Contra a IA**
3. Clique em uma de suas peças para selecioná-la
4. Clique em uma casa destacada para mover:
   - Verde = movimento simples
   - Laranja = captura
5. Capturas são obrigatórias quando disponíveis

**Cores:**
- Vermelho = Jogador 1
- Azul = Jogador 2 (ou IA)
- Coroa = peça promovida a dama

---

## Estrutura do Projeto

```
Damas/
├── main.py                          # Ponto de entrada
├── requirements.txt
│
├── src/
│   ├── config.py                    # Configurações globais
│   ├── game.py                      # Orquestração do jogo
│   ├── models/
│   │   ├── enums.py                 # Enumerações
│   │   ├── peca.py                  # Modelo de peça
│   │   └── tabuleiro.py             # Estado do tabuleiro
│   ├── services/
│   │   ├── movimento_validator.py   # Validação de movimentos
│   │   ├── capture_handler.py       # Lógica de capturas
│   │   └── promotion_handler.py     # Promoção de peças
│   ├── ia/
│   │   ├── estrategias.py           # Estratégias por heurística
│   │   └── __init__.py              # Factory da IA
│   └── gui/
│       ├── renderizador.py          # Renderização do tabuleiro
│       └── gerenciador_interface.py # Gerenciamento da UI
│
├── tests/
│   └── teste_jogo.py
│
└── scripts/
    ├── executar_jogo.bat
    └── executar_jogo.sh
```

---

## Estratégia da IA

A IA avalia e prioriza jogadas na seguinte ordem:

1. Capturas múltiplas em sequência
2. Promoção a dama
3. Movimentos seguros (evita exposição)
4. Movimento aleatório como fallback

---

## Exemplos de Uso Programático

```python
from src.game import Jogo

jogo = Jogo()
jogo.selecionar_peca(2, 1)
print(jogo.movimentos_validos)
jogo.mover_peca(2, 1, 3, 0)

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

**IA jogando rápido demais**

Aumente o delay em `main.py`:
```python
gui.janela.after(1000, ...)  # valor em milissegundos
```

---

## Melhorias Futuras

- [ ] Diferentes níveis de dificuldade da IA
- [ ] Salvar e carregar partidas
- [ ] Modo de treino com dicas visuais
- [ ] Estatísticas e histórico de partidas
- [ ] Efeitos sonoros

---

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido por **Allan Giaretta**.
