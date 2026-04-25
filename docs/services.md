# Services (Regras)

Os **services** implementam as **regras de damas** — lógica que valida, executa e detecta fim de jogo.

## MovimentoValidator (movimento_validator.py)

Valida quais movimentos são legais para uma peça.

```python
class MovimentoValidator:
    def __init__(self, tabuleiro: Tabuleiro):
        self.tabuleiro = tabuleiro
    
    def obter_movimentos_validos_para_peca(self, peca: Peca) -> List[Tuple[int, int]]:
        """
        Retorna lista de (linha, coluna) válidas.
        
        REGRA CRUCIAL: Se há capturas disponíveis para o jogador,
        SOMENTE movimentos de captura são retornados.
        """
        
        # Se há capturas disponíveis para este jogador,
        # retorna SOMENTE as capturas (captura obrigatória)
        if self.jogador_tem_capturas(peca.jogador):
            return self.encontrar_capturas_para_peca(peca)
        
        # Caso contrário, retorna movimentos normais
        return self._obter_movimentos_normais(peca)
    
    def jogador_tem_capturas(self, jogador: Jogador) -> bool:
        """Verifica se o jogador pode fazer alguma captura."""
        # Itera todas as peças do jogador
        # Se alguma tem captura possível, retorna True
    
    def encontrar_capturas_para_peca(self, peca: Peca) -> List[Tuple[int, int]]:
        """Retorna apenas os movimentos que capturam peças inimigas."""
```

### Regra de Captura Obrigatória

Se o jogador **pode capturar**, ele **deve capturar**. Não há escolha.

```python
# Exemplo:
movimentos = jogo.obter_movimentos_validos_para_peca(peca)

# Se jogo_tem_capturas() == True:
#   movimentos = [apenas capturas]
# Caso contrário:
#   movimentos = [movimentos normais]
```

---

## CaptureHandler (capture_handler.py)

Executa capturas e detecta sequências.

```python
class CaptureHandler:
    def __init__(self, tabuleiro: Tabuleiro):
        self.tabuleiro = tabuleiro
    
    def executar_captura(self, peca: Peca, linha_dest: int, col_dest: int) -> Peca:
        """
        Remove a peça capturada entre posição atual e destino.
        Retorna a peça capturada (para desfazer depois).
        """
        # Calcula o meio do caminho
        linha_captura = (peca.linha + linha_dest) // 2
        col_captura = (peca.coluna + col_dest) // 2
        
        peca_capturada = self.tabuleiro.obter_peca(linha_captura, col_captura)
        
        # Remove do tabuleiro
        self.tabuleiro.mover_peca(peca_capturada, -1, -1)
        
        return peca_capturada
    
    def detectar_capturas_sequenciais(self, peca: Peca) -> List[Tuple[int, int]]:
        """
        Após uma captura, verifica se a mesma peça pode capturar novamente.
        
        Retorna:
        - Lista de capturas possíveis (jogo continua com mesma peça)
        - [] (turno encerra, passar para próximo jogador)
        """
```

### Captura Sequencial (Multi-Jump)

Quando uma peça captura e pode capturar novamente imediatamente:

```
Posição inicial:
    0   1   2
0   ·   🔴  ·
1   ·   ·   🔵

Vermelha em (0,1) pula azul em (1,2) → vai para (2,3)?

Se em (2,3) pode pular outra peça → captura continua!
Turno não muda, peça fica selecionada.
```

---

## PromotionHandler (promotion_handler.py)

Promove peças a dama quando atingem o final do tabuleiro.

```python
class PromotionHandler:
    def verificar_promocao(self, peca: Peca, jogador_atual: Jogador) -> bool:
        """
        Promove peça a dama se atingiu o final.
        
        Retorna:
        - True: houve promoção
        - False: sem promoção
        """
        if jogador_atual == Jogador.JOGADOR1 and peca.linha == 7:
            peca.promover()
            return True
        elif jogador_atual == Jogador.JOGADOR2 and peca.linha == 0:
            peca.promover()
            return True
        return False
```

### Quando Promove?

- **JOGADOR1** (vermelho, começa no topo): promove ao atingir **linha 7**
- **JOGADOR2** (azul, começa embaixo): promove ao atingir **linha 0**

### Behavior

A promoção é **automática**. Não há escolha — se a peça chega lá, vira dama imediatamente.

---

**Próximo:** [Game (Orquestrador)](game.md)
