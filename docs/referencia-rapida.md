# 🚀 Guia de Referência Rápida - Jogo de Damas

## ⚡ Iniciar Rápido

```python
# 1. Criar um novo jogo
from src.game import Jogo
jogo = Jogo()

# 2. Selecionar uma peça
jogo.selecionar_peca(2, 1)  # linha, coluna

# 3. Ver movimentos válidos
print(jogo.movimentos_validos)

# 4. Mover peça
jogo.mover_peca(2, 1, 3, 0)  # origem e destino

# 5. Verificar fim de jogo
fim, vencedor = jogo.verificar_fim_de_jogo()
```

---

## 📖 Referência de Métodos - Classe Jogo

### Seleção e Movimento

```python
# Selecionar uma peça
selecionar_peca(linha: int, coluna: int) -> bool

# Mover uma peça
mover_peca(lin_orig: int, col_orig: int, 
           lin_dest: int, col_dest: int) -> bool

# Calcular movimentos válidos de uma peça
_calcular_movimentos_validos(linha: int, coluna: int) -> List[Tuple]

# Encontrar capturas disponíveis
_encontrar_capturas(linha: int, coluna: int) -> List[Tuple]
```

### Consultas de Estado

```python
# Contar peças de um jogador
_contar_pecas(jogador: Jogador) -> int

# Verificar fim de jogo
verificar_fim_de_jogo() -> Tuple[bool, Optional[Jogador]]

# Ver se jogador tem movimentos
_tem_movimentos_disponiveis(jogador: Jogador) -> bool
```

### Gerenciamento de Jogo

```python
# Resetar jogo
resetar()

# Acessar tabuleiro
tabuleiro: Tabuleiro

# Histórico de jogadas
historico_jogadas: List[Dict]

# Peças capturadas
piezas_capturadas_j1: int
piezas_capturadas_j2: int
```

---

## 📖 Referência de Métodos - Classe Tabuleiro

```python
# Obter peça em posição
obter_peca(linha: int, coluna: int) -> Optional[Peca]

# Colocar peça em posição
colocar_peca(peca: Peca, linha: int, coluna: int)

# Remover peça
remover_peca(linha: int, coluna: int) -> Optional[Peca]

# Verificar se casa é preta
casa_preta(linha: int, coluna: int) -> bool

# Resetar tabuleiro
resetar()

# Acessar casas
casas: List[List[Optional[Peca]]]
```

---

## 📖 Referência de Métodos - Classe Peca

```python
# Promover peça a dama
promover()

# Mover peça
mover(nova_linha: int, nova_coluna: int)

# Verificar se é dama
eh_dama() -> bool

# Atributos
jogador: Jogador
tipo: TipoPeca
linha: int
coluna: int
```

---

## 🤖 Referência de Métodos - Classe IA

```python
# Fazer movimento da IA
fazer_movimento() -> bool

# Encontrar todos os movimentos
_encontrar_todos_movimentos() -> List[Tuple]

# Avaliar movimentos
_avaliar_movimentos(movimentos: List) -> Optional[Tuple]
```

---

## 🎨 Referência de Métodos - Classe GUIJogo

```python
# Iniciar interface
iniciar()

# Atualizar tela
_atualizar_tela()

# Desenhar tabuleiro
_desenhar_tabuleiro()

# Desenhar peças
_desenhar_pecas()

# Processar clique
_ao_clicar_canvas(event)

# Novo jogo
_novo_jogo()

# Mostrar histórico
_mostrar_historico()
```

---

## 📊 Enums

### TipoPeca
```python
TipoPeca.PECA    # Peça comum
TipoPeca.DAMA    # Dama (promovida)
```

### Jogador
```python
Jogador.JOGADOR1  # Jogador 1 (vermelho)
Jogador.JOGADOR2  # Jogador 2 (azul)
```

---

## 🎯 Posições no Tabuleiro

```
     0     1     2     3     4     5     6     7
0  [  ][ P ][ P ][ P ][ P ][ P ]
1  [ P ][ P ][ P ][ P ][ P ][ P ]
2  [  ][ P ][ P ][ P ][ P ][ P ]
3  [  ][  ][  ][  ][  ][  ][  ][  ]
4  [  ][  ][  ][  ][  ][  ][  ][  ]
5  [ P ][ P ][ P ][ P ][ P ][ P ]
6  [  ][ P ][ P ][ P ][ P ][ P ]
7  [ P ][ P ][ P ][ P ][ P ][ P ]

P = Peça
[ ] = Casa preta válida
```

---

## 🔄 Fluxo de um Clique

```python
_ao_clicar_canvas(event)
    ↓
Calcular posição: linha = event.y // TAMANHO_CASA
                  coluna = event.x // TAMANHO_CASA
    ↓
if em_sequencia_captura:
    ├─ Validar movimento de captura
    └─ Passar turno após última captura
else:
    if peca_selecionada:
        ├─ Se clique válido: mover peça
        ├─ Se mesmo local: desselecionar
        └─ Se outro local: selecionar nova peça
    else:
        └─ Tentar selecionar peça
    ↓
_atualizar_tela()
```

---

## 🧮 Lógica de Validação

### Movimento Simples Válido?
```python
1. Posição dentro do tabuleiro? ✓
2. Casa é preta (preto/branco)? ✓
3. Casa está vazia? ✓
4. Peça comum: movimento para frente? ✓
5. Distância é 1 (não é captura)? ✓
```

### Captura Válida?
```python
1. Todos os critérios de movimento simples (distância = 2)? ✓
2. Há peça inimiga no meio? ✓
3. Peça comum: captura para frente? ✓
```

---

## 💾 Estrutura do Arquivo de Histórico

```python
historico_jogadas = [
    {
        'jogador': Jogador.JOGADOR1,
        'de': (2, 1),
        'para': (3, 0)
    },
    {
        'jogador': Jogador.JOGADOR2,
        'de': (5, 4),
        'para': (4, 5)
    },
    ...
]
```

---

## 🎨 Cores Personalizáveis

```python
# Em src/config.py
COR_CASA_BRANCA = "#FFD700"      # Casa clara
COR_CASA_PRETA = "#000000"       # Casa escura
COR_SELECIONADA = "#FF6B6B"      # Peça selecionada
COR_MOVIMENTO_VALIDO = "#90EE90" # Movimento simples
COR_CAPTURA = "#FFA500"          # Movimento de captura
COR_PECA_JOGADOR1 = "#FF0000"    # Peça J1
COR_PECA_JOGADOR2 = "#0000FF"    # Peça J2
COR_DAMA = "#FFD700"             # Coroa da dama
```

---

## 🔍 Debugging

### Ver estado do jogo
```python
jogo = Jogo()
print(f"Jogador atual: {jogo.jogador_atual}")
print(f"Peça selecionada: {jogo.peca_selecionada}")
print(f"Movimentos válidos: {jogo.movimentos_validos}")
print(f"J1 tem: {jogo._contar_pecas(Jogador.JOGADOR1)} peças")
print(f"J2 tem: {jogo._contar_pecas(Jogador.JOGADOR2)} peças")
```

### Ver tabuleiro
```python
for linha in range(8):
    for coluna in range(8):
        peca = jogo.tabuleiro.obter_peca(linha, coluna)
        if peca:
            print(f"({linha},{coluna}): {peca}")
```

### Simular movimento
```python
if jogo.selecionar_peca(2, 1):
    mov = jogo.movimentos_validos[0]
    if jogo.mover_peca(2, 1, mov[0], mov[1]):
        print("Movimento realizado com sucesso!")
```

---

## 🧪 Exemplos de Testes

### Teste de Movimento
```python
jogo = Jogo()
assert jogo.selecionar_peca(2, 1), "Seleção falhou"
assert len(jogo.movimentos_validos) > 0, "Sem movimentos"

mov = jogo.movimentos_validos[0]
assert jogo.mover_peca(2, 1, mov[0], mov[1]), "Movimento falhou"
assert jogo.jogador_atual == Jogador.JOGADOR2, "Turno não mudou"
```

### Teste de Captura
```python
peca_j1 = Peca(Jogador.JOGADOR1, 3, 2)
peca_j2 = Peca(Jogador.JOGADOR2, 4, 3)
jogo.tabuleiro.colocar_peca(peca_j1, 3, 2)
jogo.tabuleiro.colocar_peca(peca_j2, 4, 3)

capturas = jogo._encontrar_capturas(3, 2)
assert (5, 4) in capturas, "Captura não encontrada"
```

---

## 📌 Checklist de Desenvolvimento

- [x] Movimentos simples (peças comuns para frente)
- [x] Movimentos de dama (frente e trás)
- [x] Capturas simples
- [x] Múltiplas capturas em sequência
- [x] Promoção automática
- [x] Turnos alternados
- [x] Detecção de fim de jogo
- [x] Interface gráfica
- [x] IA do computador
- [x] Histórico de jogadas
- [x] Testes unitários
- [x] Documentação

---

## 🐛 Erros Comuns

### "AttributeError: NoneType has no attribute..."
**Causa**: Tentou acessar propriedade de None
**Solução**: Verifique se posição tem peça antes de usar

### "IndexError: list index out of range"
**Causa**: Posição fora do tabuleiro
**Solução**: Valide linha e coluna entre 0 e 7

### "TypeError: unsupported operand type(s)"
**Causa**: Tipo de dado incorreto
**Solução**: Verifique tipos de linha e coluna (devem ser int)

---

## 💡 Dicas de Performance

1. Cache movimentos válidos para evitar recálculos
2. Usar `_encontrar_capturas()` antes de permitir movimento
3. IA pode ser feita single-threaded por simplicidade
4. Tabuleiro é apenas 8x8, não há problema de performance

---

## 🔗 Referências Rápidas

| O que? | Arquivo | Método |
|--------|---------|--------|
| Mover peça | game.py | `Jogo.mover_peca()` |
| Validar movimento | game.py | `Jogo._calcular_movimentos_validos()` |
| Verificar captura | game.py | `Jogo._encontrar_capturas()` |
| Render tabuleiro | gui.py | `GUIJogo._desenhar_tabuleiro()` |
| Fazer IA jogar | ia.py | `IA.fazer_movimento()` |
| Resetar jogo | game.py | `Jogo.resetar()` |
| Histórico | game.py | `Jogo.historico_jogadas` |

---

**Última atualização: Março 2026**
