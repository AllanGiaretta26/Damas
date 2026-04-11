# 🎮 Jogo de Damas em Python

Um jogo de damas completo com interface gráfica em **tkinter**, implementado em Python com regras tradicionais e IA simples.

## 📋 Características Principais

### Funcionalidades Essenciais
✅ **Interface Gráfica Completa**
- Tabuleiro 8x8 com cores alternadas (preto e branco)
- Visualização clara de peças e damas
- Destaque visual de movimentos válidos
- Sistema intuitivo de seleção (clique nas peças)

✅ **Regras de Damas Completas**
- Peças comuns movem apenas para frente
- Damas movem para frente e para trás
- Movimentos únicos nas diagonais
- Capturas de peças adversárias
- Múltiplas capturas em sequência
- Promoção automática a dama ao alcançar o lado oposto
- Capturas obrigatórias quando disponíveis

✅ **Sistema de Jogo**
- Turnos alternados entre Jogador 1 (Vermelho) e Jogador 2 (Azul)
- Validação automática de movimentos
- Detecção de fim de jogo
- Reinício de partidas
- Histórico de jogadas

✅ **Modos de Jogo**
- 👥 Dois Jogadores (Humano vs Humano)
- 🤖 Contra a IA (Humano vs Computador)

### Recursos Extras
🎯 **IA Simples**
- Prioriza capturas
- Busca promoções
- Avalia segurança de movimentos
- Descobre capturas em sequência

📊 **Placar e Histórico**
- Contagem de peças
- Histórico de jogadas completo
- Informações em tempo real

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- tkinter (geralmente incluído no Python)

### Instalação
```bash
# Clone ou copie os arquivos para seu diretório
cd IA-VScode

# Execute o jogo
python main.py

# Ou use o script pronto
scripts/executar_jogo.bat  # Windows
scripts/executar_jogo.sh   # Linux/Mac
```

### Executar Testes
```bash
python tests/teste_jogo.py
```

### Estrutura de Pastas
```
IA-VScode/
├── main.py                 # Ponto de entrada da aplicação
├── README.md               # Este arquivo
├── requirements.txt        # Dependências
├── .gitignore             # Arquivos ignorados pelo git
│
├── src/                   # Código fonte
│   ├── models/            # Classes de domínio (SRP)
│   │   ├── enums.py       # Enumerações
│   │   ├── peca.py        # Classe Peca
│   │   └── tabuleiro.py   # Classe Tabuleiro
│   ├── services/          # Serviços especializados (SRP)
│   │   ├── movimento_validator.py  # Validação de movimentos
│   │   ├── capture_handler.py      # Gerenciamento de capturas
│   │   └── promotion_handler.py    # Promoção de peças
│   ├── ia/                # Inteligência Artificial (Strategy Pattern)
│   │   ├── estrategias.py # Estratégias por dificuldade
│   │   └── __init__.py    # Classe IA com factory
│   ├── gui/               # Interface Gráfica (SRP)
│   │   ├── renderizador.py          # Renderização
│   │   └── gerenciador_interface.py # Gerenciamento de UI
│   ├── game.py            # Classe Jogo (orquestradora)
│   └── config.py          # Configurações
│
├── tests/                 # Testes
│   ├── __init__.py
│   └── teste_jogo.py      # Testes unitários
│
├── scripts/               # Scripts utilitários
│   ├── executar_jogo.bat  # Script Windows
│   ├── executar_jogo.sh   # Script Linux
│   └── exemplos_avancados.py
│
└── docs/                  # Documentação
    ├── INDEX.md           # Índice de documentação
    ├── guides/
    │   └── comece-aqui.md
    ├── refatoracao.md
    ├── refatoracao-solid-clean-code.md
    └── ...
```

## 🎮 Como Jogar

### Iniciando o Jogo
1. Execute `python main.py`
2. Escolha o modo: "Dois Jogadores" ou "Contra a IA"
3. O jogo começará automaticamente

### Controles
- **Selecionar Peça**: Clique em uma de suas peças
- **Mover**: Clique em uma casa destacada
  - 🟢 **Verde** = Movimento simples
  - 🟠 **Laranja** = Captura
- **Desselecionar**: Clique novamente na peça selecionada
- **Captura Sequencial**: Após uma captura, se houver mais capturas disponíveis, você deve realizá-las

### Cores das Peças
- 🔴 **Vermelho** = Jogador 1 (você em "Dois Jogadores")
- 🔵 **Azul** = Jogador 2 (ou a IA)
- ♛ **Coroa** = Dama (peça promovida)

## 📐 Estrutura do Código

### Classe `Peca` (game.py)
- Representa uma peça individual
- Controla tipo (comum ou dama)
- Gerencia posição

### Classe `Tabuleiro` (game.py)
- Gerencia o estado do tabuleiro
- Coloca/remove peças
- Calcula casas válidas

### Classe `Jogo` (game.py)
- Lógica principal de regras
- Validação de movimentos
- Detecção de capturas
- Verificação de promução e fim de jogo

### Classe `GUIJogo` (gui.py)
- Interface gráfica com tkinter
- Renderização do tabuleiro
- Processamento de cliques
- Atualização visual

### Classe `IA` (ia.py)
- Estratégia de movimentos
- Avaliação de posições
- Busca de melhores jogadas

## 🎯 Regras do Jogo

### Movimento Simples (Peças Comuns)
- Peças comuns avançam apenas para as casas diagonais à frente
- Movimento permitido apenas em uma casa

### Captura
- Quando uma peça inimiga está adjacente e a casa atrás está vazia, a captura é obrigatória
- Múltiplas capturas em sequência são permitidas
- Damas podem capturar em qualquer direção diagonal

### Promoção
- Quando uma peça alcança a última linha do lado oposto, é promovida a dama
- Damas se movem em qualquer direção diagonal

### Fim de Jogo
- Ganha quem eliminar todas as peças do oponente
- Ou quem deixar o oponente sem movimentos disponíveis

## 🧠 Estratégia da IA

A IA utiliza as seguintes estratégias de priorização:

1. **Capturas em Sequência** - Busca capturar múltiplas peças
2. **Promoções** - Tenta alcançar a última linha
3. **Movimentos Seguros** - Evita posições vulneráveis
4. **Movimentos Aleatórios** - Caso nenhuma estratégia se aplique

## 🔧 Desenvolvimento

### Arquitetura
O código segue princípios de **Programação Orientada a Objetos**:
- Separação clara de responsabilidades
- Classes coesas e bem definidas
- Métodos com responsabilidade única

### Comentários
Todas as classes e métodos principais incluem:
- Docstrings explicativas
- Descrição de parâmetros
- Explicação da lógica complexa

## 📝 Exemplos de Uso

### Criar um Novo Jogo Programaticamente
```python
from src.game import Jogo, Jogador

jogo = Jogo()
# Selecionar uma peça na posição (2, 1)
jogo.selecionar_peca(2, 1)
# Ver movimentos válidos
print(jogo.movimentos_validos)
# Mover para (3, 0)
jogo.mover_peca(2, 1, 3, 0)
```

### Verificar Fim de Jogo
```python
fim_jogo, vencedor = jogo.verificar_fim_de_jogo()
if fim_jogo:
    print(f"Jogo acabou! Vencedor: {vencedor}")
```

## 🐛 Solução de Problemas

### "ModuleNotFoundError: No module named 'tkinter'"
```bash
# No Ubuntu/Debian:
sudo apt-get install python3-tk

# No Fedora:
sudo dnf install python3-tkinter

# No macOS (com brew):
brew install python-tk
```

### Jogo muito rápido (modo IA)
Ajuste o tempo em `main.py` na linha:
```python
gui.janela.after(500, ...)  # Aumentar 500 para delay maior
```

## 👨‍💻 Autor
Desenvolvido por Allan Giaretta.
