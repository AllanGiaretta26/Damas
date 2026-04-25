# Pontos de Atenção

Erros comuns, comportamentos importantes, performance e o que quebra testes.

---

## ❌ Erros Comuns

### Erro 1: Usar `mover_peca` com 2 argumentos (API antiga)

```python
# ❌ ERRADO — assinatura antiga
jogo.mover_peca(3, 2)

# ✅ CORRETO — 4 argumentos: origem + destino
jogo.selecionar_peca(2, 1)
jogo.mover_peca(2, 1, 3, 2)
```

---

### Erro 2: Acessar services diretamente

```python
# ❌ ERRADO
movimentos = jogo._movimento_validator.calcular_movimentos_validos(linha, coluna, ...)

# ✅ CORRETO — API pública aceita coordenadas
movimentos = jogo.obter_movimentos_validos_para_peca(linha, coluna)
```

**Por quê?** Mantém encapsulação e permite mudanças internas sem quebrar código externo.

---

### Erro 3: Ignorar captura obrigatória

```python
# ❌ ERRADO — Se há captura disponível, DEVE fazer captura
if peca_tem_movimento_normal():
    mover_normalmente()  # Inválido!

# ✅ CORRETO
movimentos_validos = jogo.obter_movimentos_validos_para_peca(peca)
# Se há captura, só retorna capturas (automático)
```

---

### Erro 4: Editar tabuleiro sem histórico

```python
# ❌ ERRADO — Desfazer não funcionará
jogo.tabuleiro._casas[3][3] = peca

# ✅ CORRETO — Usa fluxo oficial
jogo.mover_peca(3, 3)  # Jogo registra para histórico
```

---

### Erro 5: Chamar desfazer em modo HvH

```python
# ⚠️ Desfazer funciona, mas não faz muito sentido
# A GUI deve mostrar botão só quando modo_ia=True

if jogo.modo_ia:
    jogo.desfazer_jogada()
```

---

### Erro 6: Não respeitar tamanho 8×8

```python
# ❌ ERRADO — Índices fora de [0, 7]
jogo.tabuleiro.obter_peca(8, 8)  # IndexError

# ✅ CORRETO
if 0 <= linha < 8 and 0 <= coluna < 8:
    peca = jogo.tabuleiro.obter_peca(linha, coluna)
```

---

## 🎮 Comportamentos Importantes

### Comportamento 1: Captura Sequencial

Se uma peça captura e **pode capturar novamente**:
- ✅ Peça fica **selecionada**
- ✅ Turno **NÃO muda**
- ✅ Próximo clique **continua a captura**
- ❌ Só encerra quando não há mais capturas

```python
# Exemplo
jogo.peca_selecionada = peca
jogo.mover_peca(4, 2)  # Primeira captura

print(jogo.movimentos_validos)  # Contém (6, 4)?
# Se sim, turno ainda é do mesmo jogador
```

---

### Comportamento 2: Promoção Automática

- ✅ Automática (sem escolha)
- ✅ JOGADOR1 (vermelho): linha 7 → DAMA
- ✅ JOGADOR2 (azul): linha 0 → DAMA

```python
jogo.mover_peca(7, 1)  # JOGADOR1 no fim

# peca.tipo é agora TipoPeca.DAMA
```

---

### Comportamento 3: Movimento de Dama vs Peça

| | Comum | Dama |
|---|---|---|
| **Distância** | 1 casa | Qualquer |
| **Direção** | Só frente | Qualquer diagonal |
| **Captura** | 1 casa | Qualquer |

```python
# Peça comum em (2,2)
# Pode mover para: (3,1), (3,3)

# Dama em (2,2)
# Pode mover para: (3,1), (3,3), (4,4), (5,5), ..., (1,1), (0,0), etc.
```

---

### Comportamento 4: Turno da IA

```
1. Humano clica
   ↓
2. jogo.mover_peca(lo, co, ld, cd)
   ↓
3. callback_pos_atualizacao é chamado
   ↓
4. Callback verifica: if jogo.jogador_atual == ia.jogador
   ↓
5. Se sim: ia.fazer_movimento()
   ↓
6. Turno volta para humano
```

**Importante:** A IA nunca faz movimento se não é seu turno.

---

### Comportamento 5: Undo com IA

```python
# Desfazer UMA VEZ: apenas desfaz último movimento do humano
jogo.desfazer_jogada()

# Desfazer DUAS VEZES: desfaz IA + humano
jogo.desfazer_jogada()  # Desfaz movimento da IA
jogo.desfazer_jogada()  # Desfaz movimento do humano

# Volta ao turno do humano anterior
```

**GUI faz isso automaticamente** no botão "Desfazer" com `modo_ia=True`.

---

## ⚠️ Performance

### Minimax em Profundidade Alta

| Profundidade | Tempo | Prático |
|---|---|---|
| 1 | <50ms | ✅ |
| 2 | ~150ms | ✅ |
| 3 | ~500ms | ✅ |
| 4 | ~2s | ⚠️ |
| 5 | ~5-10s | ❌ |

**Recomendação:** Depth 3 (Normal) é bom equilíbrio. Depth 5 (Difícil) é lento.

---

### Não Modificar Jogo Durante IA

```python
# ❌ ERRADO
ia.fazer_movimento()
ia.fazer_movimento()  # Pode corromper

# ✅ CORRETO
ia.fazer_movimento()
# Aguarda callback avisar que é turno da IA novamente
```

---

### Minimax com Captura Ordenada

Bom: movimentos de captura são testados primeiro → **poda alfa-beta mais eficiente**.

```python
# Internamente, CaptureHandler prioriza:
# 1. Capturas (movimentos com ganho material)
# 2. Depois movimentos normais

# Isso faz minimax mais rápido
```

---

## 🧪 O Que Quebra Testes

Se você mudar isto, testes falham:

| O que mudou | Impacto |
|---|---|
| Linha de promoção (JOGADOR1 de 7 para 6) | ❌ Testes quebram |
| Movimento de dama (qualquer diagonal → só 2 casas) | ❌ Testes quebram |
| Captura obrigatória (sempre obrigatória → opcional) | ❌ Testes quebram |
| Undo (o que salva no histórico) | ❌ Testes quebram |
| Tamanho do tabuleiro (8×8 → 10×10) | ❌ Testes quebram |
| Número inicial de peças (3 fileiras → 4) | ❌ Testes quebram |

**Solução:** Sempre rode `python tests/teste_jogo.py` após mudanças estruturais.

---

## 🔧 Mudanças Seguras

Estas mudanças **não quebram testes**:

| O que mudou | Impacto |
|---|---|
| Cores no config.py | ✅ Seguro |
| Tamanho do canvas | ✅ Seguro |
| Labels de botões | ✅ Seguro |
| Tipos de IA nomes | ✅ Seguro (se mantém enum) |
| Métodos privados (_) | ✅ Seguro (não usados externamente) |

---

## 📋 Checklist para Novas Features

Antes de adicionar algo novo:

- [ ] É uma mutação? → Adicionar ao `delta` de histórico
- [ ] É undo-ável? → Implementar reversão em `desfazer_jogada()`
- [ ] Segue dependências? → Não importar GUI em models
- [ ] Tem tipo hint? → `def mover(...) -> bool:`
- [ ] Testei? → `python tests/teste_jogo.py`
- [ ] GUI atualiza? → Chamou `_renderizar()` ou callback

---

## 📚 Referências

- [Architecture](arquitetura.md) — Como se encaixa
- [Tests](../tests/teste_jogo.py) — Exemplos práticos
- [Config](../src/config.py) — Constantes visuais

