# 🎮 VISÃO GERAL DO JOGO DE DAMAS

## 📊 Arquitetura do Projeto

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃          JOGO DE DAMAS EM PYTHON             ┃
┃          (Interface com tkinter)             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
           ┌─────────────────────────┐
           │      main.py            │
           │  (Ponto de entrada)     │
           └────────────┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │GUI (tkinter)  │ Lógica  │    │    IA   │
   └──────────┘    │ do Jogo │    └─────────┘
        │          └────┬────┘         │
        │               │              │
   ┌────▼────────┐  ┌───▼────┐   ┌────▼─────┐
   │src/gui.py   │  │Tabuleiro│   │src/ia.py │
   │ - Render    │  │ - Peças │   │- Estratégia
   │ - Eventos   │  │ - Regras│   │- Avaliação
   └─────────────┘  └────────┘    └──────────┘
        │              │
        │          ┌───▼────────┐
        │          │ src/game.py│
        │          │ - Jogo     │
        │          │ - Peca     │
        │          │ - Tabuleiro│
        │          └────────────┘
        │
   ┌────▼─────────────────┐
   │   src/config.py      │
   │  - Cores             │
   │  - Temas             │
   │  - Configurações     │
   └──────────────────────┘
```

---

## 🔄 Fluxo de Execução

```
                    INÍCIO
                      │
                      ▼
         ┌──────────────────────┐
         │ Tela de Seleção      │
         │ de Modo de Jogo      │
         └─┬────────────────┬───┘
           │                │
      [2 Jogadores]   [vs IA]
           │                │
           ▼                ▼
    ┌─────────────┐  ┌─────────────┐
    │ GUIJogo     │  │ GUIJogo +   │
    │ (Humano     │  │ IA (Humano  │
    │  vs         │  │ vs Comp.)   │
    │  Humano)    │  └──────┬──────┘
    └──────┬──────┘         │
           │                │
           └────────┬───────┘
                    │
              ┌─────▼──────┐
              │ Loop Jogo  │
              └──────┬──────┘
                    │
        ┌──────────┬┴┬──────────┐
        │          │ │          │
        ▼          ▼ ▼          ▼
    Aguardando  Humano Computador Finalizando
    Clique      Seleciona Movimento
        │        └──┬──┘   │
        ▼           ▼      ▼
    Clique Movimento IA Fazer Movimento
    em x,y   Válido?     │
    │        │   │       │
    ├────────▼───┼──────►┼────────┐
    │        SIM │       │        │
    │        │   │       │        │
    │        ▼   ▼       ▼        │
    │    Mover Atualizar Tela    │
    │      Peça   │        │      │
    │      │      │        │      │
    │      └──────┼────────┘      │
    │             │               │
    │             ▼               │
    │      ┌─────────────────┐    │
    │      │ Verificar      │    │
    │      │ Fim de Jogo?   │    │
    │      └───┬──────┬──────┘    │
    │          │      │          │
    │     [SIM] │ [NÃO]│          │
    │          ▼      ▼          │
    │      Fim   Próximo Turno   │
    │      │        │            │
    │      │        └────────────┤
    │      │                     │
    │      └────────┬────────────┘
    │             │
    ├─────────────▼────────────┐
    │                          │
    ▼                          ▼
 FIM COM         JOGAR NOVAMENTE?
 VENCEDOR        NO: FIM
                 SIM: VOLTA AO INÍCIO
```

---

## 📚 Estrutura de Pastas

```
IA-VScode/
│
├── 🟢 CÓDIGO PRINCIPAL (5 arquivos)
│   ├── main.py                    ████ 150 linhas
│   └── src/
│       ├── games.py               █████ 420 linhas
│       ├── gui.py                 ████ 320 linhas
│       ├── ia.py                  ███ 210 linhas
│       ├── config.py              ██ 90 linhas
│       └── __init__.py
│
├── 🔵 TESTES E EXEMPLOS (2 arquivos)
│   ├── teste_jogo.py              ████ 250 linhas ✅
│   └── exemplos_avancados.py      ████ 280 linhas ✅
│
├── 📖 DOCUMENTAÇÃO (4 arquivos)
│   ├── README.md                  ████ 250 linhas
│   ├── ESTRUTURA.md               ███ 200 linhas
│   ├── RESUMO.md                  ███ 200 linhas
│   └── REFERENCIA_RAPIDA.md       ████ 300 linhas
│
├── ⚙️ CONFIGURAÇÃO (1 arquivo)
│   └── requirements.txt
│
├── ⚡ SCRIPTS (2 arquivos)
│   ├── executar_jogo.bat
│   └── executar_jogo.sh
│
└── 📋 REFERÊNCIAS (2 arquivos)
    ├── ENTREGA.md
    └── VISAO_GERAL.md (este arquivo)
```

---

## 🎮 Interface do Jogo

```
╔═══════════════════════════════════════════════════════════╗
║                   JOGO DE DAMAS                          ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Turno: Jogador 1 (Vermelho)  Peças: J1:12 J2:12        ║
║  Capturadas: J1:0 J2:0                                   ║
║                                                           ║
║  ┌──────────────────────────────────────────────────┐   ║
║  │  ⊟  │  ⊟  │  ⊟  │  ⊟  │  ⊟  │  ⊟  │           │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │     │  ⊟  │     │  ⊟  │     │  ⊟  │     │      │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │  ⊟  │     │  ⊟  │     │  ⊟  │     │  ⊟  │      │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │     │     │     │     │     │     │     │      │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │     │     │     │     │     │     │     │      │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │  ●  │     │  ●  │     │  ●  │     │  ●  │      │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │     │  ●  │     │  ●  │     │  ●  │     │  ●   │   ║
║  ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
║  │  ●  │     │  ●  │     │  ●  │     │  ●  │      │   ║
║  └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
║                                                           ║
║  [Novo Jogo]  [Histórico]  [Sair]                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Legenda:
⊟ = Vermelho (Jogador 1)
● = Azul (Jogador 2)
♛ = Dama (Promovida)
```

---

## 📊 Estrutura de Classes

```
Hierarquia de Héritabilidade:

TipoPeca (Enum)
├── PECA
└── DAMA

Jogador (Enum)
├── JOGADOR1
└── JOGADOR2

Peca
├── jogador: Jogador
├── tipo: TipoPeca
├── linha: int
├── coluna: int
└── métodos: promover(), mover(), eh_dama()

Tabuleiro
├── casas[8][8]: List[List[Optional[Peca]]]
└── métodos: obter_peca(), colocar_peca(), remover_peca(), casa_preta()

Jogo
├── tabuleiro: Tabuleiro
├── jogador_atual: Jogador
├── peca_selecionada: Optional[Peca]
├── movimentos_validos: List[Tuple]
├── historico_jogadas: List[Dict]
├── piezas_capturadas_j1: int
├── piezas_capturadas_j2: int
├── em_sequencia_captura: bool
└── muitos métodos... (80+)

GUIJogo
├── janela: tk.Tk
├── jogo: Jogo
├── canvas: tk.Canvas
├── TAMANHO_CASA: int
├── COR_*: str (cores)
└── métodos de renderização

IA
├── jogo: Jogo
├── jogador: Jogador
└── métodos de estratégia
```

---

## 🎯 Estados do Jogo

```
Estado: JOGO_INICIADO
├── Ação Usuário: Clica peça
├── Condição: Peça pertence ao jogador atual?
│
├─ SIM ─► Estado: PECA_SELECIONADA
│        ├── Ação Usuário: Clica movimento válido
│        ├── Ação Usuário: Clica outra peça
│        └── Ação Usuário: Clica mesma peça (desselecionar)
│
└─ NÃO ─► Estado: JOGO_INICIADO (não faz nada)

Estado: PECA_SELECIONADA
├── Ação: Move para posição válida
│   ├── Executar movimento
│   ├── Processar captura (se houver)
│   ├── Verificar promoção
│   ├── Tem captura sequencial?
│   │
│   ├─ SIM ─► Estado: PECA_SELECIONADA (continua turno)
│   └─ NÃO ─► Estado: TURNO_PROXIMO
│
└── Ação: Selecionar outra peça ou desselecionar

Estado: TURNO_PROXIMO
├── Próximo jogador
├── Se IA: fazer movimento (automático)
└── Voltar Estado: JOGO_INICIADO

Estado: JOGO_FINALIZADO
├── Mostrar vencedor
├── Ação: Novo jogo ─► JOGO_INICIADO
└── Ação: Sair ─► FIM
```

---

## 🔄 Ciclo de um Movimento Completo

```
1️⃣ SELEÇÃO
   Usuario clica em peça
           │
           ▼
   selecionar_peca(linha, coluna)
           │
           ├─ Verifica si peça pertence a jogador atual
           ├─ Calcula movimentos válidos
           └─ Retorna lista de de posições válidas

2️⃣ VISUALIZAÇÃO
   Destaca movimentos válidos no canvas
   Verde: movimentos simples
   Laranja: capturas

3️⃣ EXECUÇÃO
   Usuario clica em movimento válido
           │
           ▼
   mover_peca(origem, destino)
           │
           ├─ Valida movimento
           ├─ Move peça no tabuleiro
           ├─ Se passou 2 casas: captura peça do meio
           ├─ Verifica promoção
           ├─ Registra no histórico
           └─ Verifica captura sequencial

4️⃣ FINALIZAÇÃO (sem captura seq.)
   _proxima_jogada()
           │
           ├─ Alterna jogador
           ├─ Verifica fim de jogo
           └─ Volta ao estado JOGO_INICIADO
```

---

## 💾 Formato de Dados

### Peca (Objeto)
```python
{
    jogador: Jogador.JOGADOR1,
    tipo: TipoPeca.PECA,    # ou TipoPeca.DAMA
    linha: 2,
    coluna: 1
}
```

### Movimento Válido (Tupla)
```python
(linha_destino, coluna_destino)
# Exemplo:
(3, 0), (3, 2)
```

### Jogada Registrada (Dicionário)
```python
{
    'jogador': Jogador.JOGADOR1,
    'de': (2, 1),
    'para': (3, 0)
}
```

### Estado do Tabuleiro
```python
casas[8][8]  # Lista 2D
# Cada posição contém:
#   None (vazio)
#   ou Peca (peça)
```

---

## 🎨 Sistema de Cores

```
Interface         RGB        Hex
──────────────────────────────────
Casa Branca      255,215,0  #FFD700
Casa Preta       0,0,0      #000000
Peça J1 (Vermel) 255,0,0    #FF0000
Peça J2 (Azul)   0,0,255    #0000FF
Selecionada      255,107,107#FF6B6B
Movimento Vál.   144,238,144#90EE90
Captura          255,165,0  #FFA500
Coroa Dama       255,215,0  #FFD700
Fundo            204,204,204#CCCCCC
```

---

## 🚀 Sequência de Inicialização

```
python main.py
     │
     ▼
AplicacaoDamas.__init__()
     │
     ├─ Criar janela tkinter
     ├─ Criar tela de seleção
     └─ Mostrar raiz.mainloop()
     
Usuario seleciona modo
     │
     ├─► "Humano vs Humano"
     │       │
     │       ▼
     │   janela_jogo = tk.Tk()
     │   gui = GUIJogo(janela_jogo)
     │   gui.iniciar()
     │
     └─► "Humano vs IA"
         │
         ▼
         janela_jogo = tk.Tk()
         gui = GUIJogo(janela_jogo)
         ia = IA(gui.jogo)
         gui.iniciar()
         
(IA conectada ao loop de jogo)
```

---

## 📈 Complexidade do Código

```
Linhas por componente:

Lógica do Jogo
└── src/game.py ████████████████████ 420 linhas
    ├── Classe Jogo ████████████████ 350 linhas
    ├── Classe Tabuleiro ██████ 80 linhas
    └── Classe Peca ██ 30 linhas

Interface Gráfica
└── src/gui.py ████████████████ 320 linhas
    ├── Classe GUIJogo ████████████████ 320 linhas

Inteligência Artificial
└── src/ia.py ██████████ 210 linhas
    └── Classe IA ██████████ 210 linhas

Configuração
└── src/config.py ███ 90 linhas

Testes
└── teste_jogo.py ███████████ 250 linhas

Total de Código Fonte: ~1,290 linhas
Total com Testes: ~1,540 linhas
Total com Documentação: ~3,500 linhas
```

---

## ✨ Destaques Técnicos

### 🔐 Validação
- ✅ Posição dentro do tabuleiro
- ✅ Casa não ocupada
- ✅ Movimento apenas diagonais
- ✅ Peça comum frente, dama ambas
- ✅ Capturas obrigatórias

### 🧠 Estratégia IA
- ✅ BFS (ampla) para encontrar movimentos
- ✅ Scoring para avaliar posições
- ✅ Greedy algorithm para melhor movimento
- ✅ Look-ahead para capturas sequenciais

### 🎨 Interface
- ✅ Renderização eficiente com Canvas
- ✅ Events handling não-bloqueante
- ✅ Atualização visual em tempo real
- ✅ Feedback imediato ao usuário

---

**PROJETO COMPLETO E PROFISSIONAL** ✨

Versão 1.0 - Março 2026
