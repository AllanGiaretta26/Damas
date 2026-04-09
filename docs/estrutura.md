# 📁 Estrutura do Projeto

```
IA-VScode/
│
├── 📄 main.py                 # Ponto de entrada principal da aplicação
├── 📄 README.md               # Documentação completa do projeto
├── 📄 requirements.txt        # Dependências do projeto
├── 📄 executar_jogo.bat       # Script para executar no Windows
├── 📄 executar_jogo.sh        # Script para executar em Linux/macOS
├── 📄 teste_jogo.py          # Suite de testes unitários
├── 📄 exemplos_avancados.py  # Exemplos de uso avançado
│
└── 📁 src/                    # Código-fonte do jogo
    ├── 📄 __init__.py         # Pacote Python
    ├── 📄 game.py             # Lógica principal do jogo
    ├── 📄 gui.py              # Interface gráfica (tkinter)
    ├── 📄 ia.py               # IA para jogar contra computador
    └── 📄 config.py           # Configurações e temas
```

## 📚 Descrição dos Arquivos

### Arquivos Principais

#### `main.py` (150 linhas)
**Responsabilidade**: Ponto de entrada da aplicação
- Cria a tela inicial de seleção de modo
- Gerencia inicialização da GUI
- Integra a IA com a interface

**Classes Principais**:
- `AplicacaoDamas`: Interface de seleção de modo de jogo

#### `src/game.py` (420 linhas)
**Responsabilidade**: Lógica central do jogo
- Implementa todas as regras de damas
- Valida movimentos
- Determina fim de jogo

**Classes Principais**:
- `Peca`: Representa uma peça individual (comum ou dama)
- `Tabuleiro`: Gerencia o estado do tabuleiro 8x8
- `Jogo`: Lógica completa com turnos, capturas, promoções

**Métodos Críticos**:
- `selecionar_peca()`: Seleciona uma peça e calcula movimentos válidos
- `mover_peca()`: Executa um movimento completo
- `_encontrar_capturas()`: Localiza capturas obrigatórias
- `verificar_fim_de_jogo()`: Detecta condições de vitória

#### `src/gui.py` (320 linhas)
**Responsabilidade**: Interface gráfica com tkinter
- Renderiza o tabuleiro visualmente
- Gerencia eventos de mouse
- Atualiza estado visual

**Classe Principal**:
- `GUIJogo`: Gerencia toda a interface visual

**Métodos Críticos**:
- `_desenhar_tabuleiro()`: Renderiza o tabuleiro com cores
- `_atualizar_tela()`: Atualiza a visualização completa
- `_ao_clicar_canvas()`: Processa cliques do jogador

#### `src/ia.py` (210 linhas)
**Responsabilidade**: IA para jogar contra o computador
- Encontra movimentos legais
- Avalia qualidade de movimentos
- Prioriza capturas e promoções

**Classe Principal**:
- `IA`: Implementa estratégia de jogo

**Métodos Críticos**:
- `fazer_movimento()`: Executa um movimento da IA
- `_avaliar_movimentos()`: Escolhe o melhor movimento
- `_escolher_melhor_captura()`: Prioriza capturas em sequência

#### `src/config.py` (90 linhas)
**Responsabilidade**: Configurações e temas
- Define cores e tamanhos
- Fornece temas alternativos
- Permite personalização

### Arquivos de Apoio

#### `teste_jogo.py` (250 linhas)
Suite completa de testes:
- Teste de inicialização
- Teste de movimento simples
- Teste de captura
- Teste de promoção
- Teste de movimentos de dama
- Teste de fim de jogo
- Teste de histórico

#### `exemplos_avancados.py` (280 linhas)
Exemplos práticos de uso:
1. Simular IA vs IA
2. Criar tabuleiro customizado
3. Analisar movimentos disponíveis
4. Exibir histórico de jogo
5. Testar regras específicas

## 📊 Fluxo da Aplicação

```
main.py (executar)
    ↓
Tela de seleção de modo
    ├─→ "Dois Jogadores" → GUIJogo
    │                       ↓
    │                   Loop de jogo
    │                   (cliques do jogador)
    │
    └─→ "Contra IA" → GUIJogo + IA
                      ↓
                  Loop de jogo
                  (cliques do jogador + IA)
```

## 🔄 Fluxo de um Movimento

```
Clique do Jogador
    ↓
_ao_clicar_canvas()
    ├─→ Calcula posição (linha, coluna)
    ├─→ Checa se há peça selecionada
    │
    ├─→ [Não] Tenta selecionar peça
    │   ├─→ selecionar_peca()
    │   ├─→ _calcular_movimentos_validos()
    │   └─→ _desenhar_tabuleiro() (destaque)
    │
    └─→ [Sim] Valida movimento
        ├─→ Checa se está em lista de movimentos válidos
        ├─→ mover_peca()
        │   ├─→ Processa captura (se houver)
        │   ├─→ Verifica promoção
        │   ├─→ Registra no histórico
        │   └─→ Passa turno (se não for captura sequencial)
        └─→ _atualizar_tela()
```

## 🎮 Estados do Jogo

```
ESPERANDO SELEÇÃO
    ↓ (jogador clica em sua peça)
PEÇA SELECIONADA
    ├─→ Mostrar movimentos válidos
    ├─→ (jogador clica em movimento válido)
    └─→ PROCESSANDO MOVIMENTO
        ├─→ Validar movimento
        ├─→ Executar movimento
        ├─→ Capturar peça (se houver)
        ├─→ Verificar promoção
        ├─→ Verificar captura sequencial
        │
        ├─→ [Captura sequencial] PEÇA SELECIONADA
        │   ├─→ Mostrar próximas capturas
        │   └─→ Aguardar próximo movimento
        │
        └─→ [Sem captura sequencial] PASSAR TURNO
            ├─→ Mudar jogador atual
            ├─→ Verificar fim de jogo
            ├─→ [IA] Fazer movimento (automático)
            └─→ ESPERANDO SELEÇÃO
```

## 🏗️ Arquitetura de Classes

### Hierarquia de Responsabilidades

```
Jogo
├── Tabuleiro (composição)
│   └── Peca[64] (composição)
│       ├── Jogador (enum)
│       └── TipoPeca (enum)
│
├── Histórico (lista de movimentos)
└── Estados (turno, peça selecionada, etc)

GUIJogo
├── Jogo (composição)
├── Canvas (tkinter)
└── Widgets (botões, labels)

IA
└── Jogo (referência)
    └── Tabuleiro (acesso via jogo)
```

### Diagrama de Classes Simplificado

```
┌─────────────┐
│   Peca      │
├─────────────┤
│ jogador     │
│ tipo        │
│ linha       │
│ coluna      │
├─────────────┤
│ promover()  │
│ mover()     │
│ eh_dama()   │
└─────────────┘

┌─────────────┐
│  Tabuleiro  │
├─────────────┤
│ casas[8][8] │
├─────────────┤
│ obter_peca()│
│ colocar()   │
│ remover()   │
└─────────────┘

┌─────────────┐
│    Jogo     │
├─────────────┤
│ tabuleiro   │
│ jogador_at  │
│ mov_validos │
├─────────────┤
│ selecionar()│
│ mover_peca()│
│ verificar() │
└─────────────┘
```

## 💾 Tamanho Total de Código

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| main.py | 150 | Ponto de entrada |
| game.py | 420 | Lógica do jogo |
| gui.py | 320 | Interface gráfica |
| ia.py | 210 | IA do computador |
| config.py | 90 | Configurações |
| teste_jogo.py | 250 | Testes unitários |
| exemplos_avancados.py | 280 | Exemplos de uso |
| **TOTAL** | **~1720** | **Código bem estruturado** |

## 🎨 Design Patterns Utilizados

1. **MVC (Model-View-Controller)**
   - Model: `game.py` (lógica)
   - View: `gui.py` (interface)
   - Controller: `main.py` (orquestração)

2. **Composition**
   - `Jogo` compõe `Tabuleiro`
   - `Tabuleiro` compõe `Peca`

3. **Strategy Pattern**
   - `IA` implementa estratégia de movimentos

4. **Enum Pattern**
   - `TipoPeca` e `Jogador` como enums seguros

## 📦 Dependências

- **Python 3.7+**
- **tkinter** (incluído com Python)

## 🧪 Cobertura de Testes

Todos os testes passam ✅

- ✅ Inicialização do jogo
- ✅ Movimentos simples
- ✅ Capturas
- ✅ Promoções
- ✅ Movimentos de dama
- ✅ Detecção de fim de jogo
- ✅ Histórico de jogadas

---

**Projeto bem estruturado, modular e extensível! 🎉**
