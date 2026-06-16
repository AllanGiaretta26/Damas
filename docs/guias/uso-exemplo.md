# Exemplos de uso

Exemplos programáticos mínimos para usar `Jogo` e `IA` sem interface gráfica.

## Movimento simples

```python
from src.game import Jogo
from src.models import Jogador

jogo = Jogo()

assert jogo.jogador_atual == Jogador.JOGADOR1
assert jogo.selecionar_peca(5, 0)
assert (4, 1) in jogo.movimentos_validos
assert jogo.mover_peca(5, 0, 4, 1)
assert jogo.jogador_atual == Jogador.JOGADOR2
```

## Captura

```python
from src.game import Jogo
from src.models import Peca, Jogador

jogo = Jogo()
jogo.tabuleiro._casas = [[None] * 8 for _ in range(8)]

vermelha = Peca(Jogador.JOGADOR1, 5, 0)
azul = Peca(Jogador.JOGADOR2, 4, 1)
jogo.tabuleiro.colocar_peca(vermelha, 5, 0)
jogo.tabuleiro.colocar_peca(azul, 4, 1)

assert jogo.jogador_tem_capturas(Jogador.JOGADOR1)
assert jogo.selecionar_peca(5, 0)
assert jogo.mover_peca(5, 0, 3, 2)
assert jogo.tabuleiro.obter_peca(4, 1) is None
assert jogo.tabuleiro.obter_peca(3, 2) is vermelha
```

## Captura sequencial

```python
from src.game import Jogo
from src.models import Peca, Jogador

jogo = Jogo()
jogo.tabuleiro._casas = [[None] * 8 for _ in range(8)]

vermelha = Peca(Jogador.JOGADOR1, 5, 0)
azul1 = Peca(Jogador.JOGADOR2, 4, 1)
azul2 = Peca(Jogador.JOGADOR2, 2, 3)
jogo.tabuleiro.colocar_peca(vermelha, 5, 0)
jogo.tabuleiro.colocar_peca(azul1, 4, 1)
jogo.tabuleiro.colocar_peca(azul2, 2, 3)

assert jogo.selecionar_peca(5, 0)
assert jogo.mover_peca(5, 0, 3, 2)
assert jogo.em_sequencia_captura
assert jogo.jogador_atual == Jogador.JOGADOR1

assert jogo.mover_peca(3, 2, 1, 4)
assert not jogo.em_sequencia_captura
assert jogo.jogador_atual == Jogador.JOGADOR2
```

## Promoção

```python
from src.game import Jogo
from src.models import Peca, Jogador, TipoPeca

jogo = Jogo()
jogo.tabuleiro._casas = [[None] * 8 for _ in range(8)]

peca = Peca(Jogador.JOGADOR1, 1, 0)
jogo.tabuleiro.colocar_peca(peca, 1, 0)

assert jogo.selecionar_peca(1, 0)
assert jogo.mover_peca(1, 0, 0, 1)
assert peca.tipo == TipoPeca.DAMA
```

## Desfazer

```python
from src.game import Jogo

jogo = Jogo()
assert jogo.selecionar_peca(5, 0)
assert jogo.mover_peca(5, 0, 4, 1)

assert jogo.desfazer_jogada()
assert jogo.tabuleiro.obter_peca(5, 0) is not None
assert jogo.tabuleiro.obter_peca(4, 1) is None
```

## IA

```python
from src.game import Jogo
from src.ia import IA
from src.models import Jogador

jogo = Jogo()
jogo.modo_ia = True

ia = IA(jogo, dificuldade="medio", jogador=Jogador.JOGADOR2)

assert jogo.selecionar_peca(5, 0)
assert jogo.mover_peca(5, 0, 4, 1)
assert jogo.jogador_atual == ia.jogador

ia.fazer_movimento()
```

## Fim de jogo

```python
from src.game import Jogo
from src.models import Jogador

jogo = Jogo()
for linha in range(8):
    for coluna in range(8):
        peca = jogo.tabuleiro.obter_peca(linha, coluna)
        if peca and peca.jogador == Jogador.JOGADOR2:
            jogo.tabuleiro.remover_peca(linha, coluna)

fim, vencedor = jogo.verificar_fim_de_jogo()
assert fim
assert vencedor == Jogador.JOGADOR1
```

## Próximo documento

[Pontos de atenção](pontos-atencao.md)
