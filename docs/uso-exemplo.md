# Exemplos de Uso

Como usar a classe `Jogo` e a IA programaticamente.

## Exemplo 1: Jogo Básico

```python
from src.game import Jogo
from src.models import Jogador

jogo = Jogo()

# Obter movimentos válidos para uma peça em (2, 1)
movimentos = jogo.obter_movimentos_validos_para_peca(2, 1)
print(movimentos)  # [(3, 0), (3, 2)] ou similar

# Selecionar peça e mover
jogo.selecionar_peca(2, 1)
if (3, 0) in movimentos:
    jogo.mover_peca(2, 1, 3, 0)
    print(f"Turno atual: {jogo.jogador_atual}")  # JOGADOR2
```

---

## Exemplo 2: Com IA

```python
from src.game import Jogo
from src.ia import IA
from src.models import Jogador

jogo = Jogo()
jogo.modo_ia = True

# Criar IA nível difícil (chave minúscula, sem acento)
ia = IA(jogo, dificuldade="dificil", jogador=Jogador.JOGADOR2)

# Humano faz primeiro movimento
jogo.selecionar_peca(2, 1)
jogo.mover_peca(2, 1, 3, 0)

# IA faz seu movimento
ia.fazer_movimento()

print(f"Turno: {jogo.jogador_atual}")  # JOGADOR1 novamente
```

---

## Exemplo 3: Captura

```python
from src.game import Jogo
from src.models import Peca, Jogador

jogo = Jogo()
jogo.tabuleiro._casas = [[None]*8 for _ in range(8)]

peca_vermelha = Peca(Jogador.JOGADOR1, 2, 0)
peca_azul = Peca(Jogador.JOGADOR2, 3, 1)

jogo.tabuleiro._casas[2][0] = peca_vermelha
jogo.tabuleiro._casas[3][1] = peca_azul

# Verifica se há captura
tem_captura = jogo.jogador_tem_capturas(Jogador.JOGADOR1)
print(tem_captura)  # True

# Executa captura: (2,0) → (4,2), passa por cima de (3,1)
jogo.selecionar_peca(2, 0)
jogo.mover_peca(2, 0, 4, 2)

print(jogo.tabuleiro.obter_peca(3, 1))  # None (capturada)
print(jogo.tabuleiro.obter_peca(4, 2))  # peca_vermelha
```

---

## Exemplo 4: Captura Sequencial

```python
from src.game import Jogo
from src.models import Peca, Jogador

jogo = Jogo()
jogo.tabuleiro._casas = [[None]*8 for _ in range(8)]

vermelha = Peca(Jogador.JOGADOR1, 0, 0)
azul1    = Peca(Jogador.JOGADOR2, 1, 1)
azul2    = Peca(Jogador.JOGADOR2, 3, 3)

jogo.tabuleiro._casas[0][0] = vermelha
jogo.tabuleiro._casas[1][1] = azul1
jogo.tabuleiro._casas[3][3] = azul2

# Primeira captura: (0,0) → (2,2)
jogo.selecionar_peca(0, 0)
jogo.mover_peca(0, 0, 2, 2)

# Turno NÃO mudou — sequência de captura ativa
print(jogo.jogador_atual)       # JOGADOR1
print(jogo.em_sequencia_captura)  # True

# Segunda captura
jogo.mover_peca(2, 2, 4, 4)

print(jogo.jogador_atual)       # JOGADOR2 (encerrou)
```

---

## Exemplo 5: Promoção

```python
from src.game import Jogo
from src.models import Peca, Jogador, TipoPeca

jogo = Jogo()
jogo.tabuleiro._casas = [[None]*8 for _ in range(8)]

peca = Peca(Jogador.JOGADOR1, 6, 0)
jogo.tabuleiro._casas[6][0] = peca

print(peca.tipo)  # TipoPeca.PECA

# Move para linha 7 (final do tabuleiro para JOGADOR1)
jogo.selecionar_peca(6, 0)
jogo.mover_peca(6, 0, 7, 1)

print(peca.tipo)  # TipoPeca.DAMA
```

---

## Exemplo 6: Desfazer

```python
from src.game import Jogo

jogo = Jogo()

# Move 1
jogo.selecionar_peca(2, 1)
jogo.mover_peca(2, 1, 3, 0)
print(jogo.jogador_atual)  # JOGADOR2

# Move 2
jogo.selecionar_peca(5, 1)
jogo.mover_peca(5, 1, 4, 0)
print(jogo.jogador_atual)  # JOGADOR1

# Desfaz move 2
jogo.desfazer_jogada()
print(jogo.jogador_atual)  # JOGADOR2

# Desfaz move 1
jogo.desfazer_jogada()
print(jogo.jogador_atual)  # JOGADOR1
```

---

## Exemplo 7: Verificar Fim de Jogo

```python
from src.game import Jogo

jogo = Jogo()

# verificar_fim_de_jogo() retorna TUPLA (bool, Optional[Jogador])
fim, vencedor = jogo.verificar_fim_de_jogo()
print(fim)      # False (jogo novo)
print(vencedor) # None

# Após o jogo acabar:
# fim, vencedor = jogo.verificar_fim_de_jogo()
# if fim:
#     print(f"Vencedor: {vencedor}")
```

---

## Exemplo 8: Testes Procedurais

Ver [tests/teste_jogo.py](../tests/teste_jogo.py) para exemplos completos.

```python
def teste_captura_basica():
    jogo = Jogo()
    jogo.tabuleiro._casas = [[None]*8 for _ in range(8)]

    peca_vermelha = Peca(Jogador.JOGADOR1, 2, 0)
    peca_azul     = Peca(Jogador.JOGADOR2, 3, 1)
    jogo.tabuleiro._casas[2][0] = peca_vermelha
    jogo.tabuleiro._casas[3][1] = peca_azul

    jogo.selecionar_peca(2, 0)
    jogo.mover_peca(2, 0, 4, 2)

    assert jogo.tabuleiro.obter_peca(3, 1) is None
    print("[OK] Captura funciona!")

teste_captura_basica()
```

---

## Exemplo 9: Explorar Movimentos

```python
from src.game import Jogo
from src.models import Jogador

jogo = Jogo()

# Itera tabuleiro para encontrar peças do JOGADOR1
for linha in range(8):
    for coluna in range(8):
        peca = jogo.tabuleiro.obter_peca(linha, coluna)
        if peca and peca.jogador == Jogador.JOGADOR1:
            movimentos = jogo.obter_movimentos_validos_para_peca(linha, coluna)
            if movimentos:
                print(f"Peca em ({linha},{coluna}): {movimentos}")
```

---

## Exemplo 10: Simulação IA vs IA

```python
from src.game import Jogo
from src.ia import IA
from src.models import Jogador

def simular_partida():
    jogo = Jogo()
    jogo.modo_ia = True

    ia_j1 = IA(jogo, "normal",  Jogador.JOGADOR1)
    ia_j2 = IA(jogo, "dificil", Jogador.JOGADOR2)

    for turno in range(200):
        fim, vencedor = jogo.verificar_fim_de_jogo()
        if fim:
            print(f"Fim em {turno} turnos. Vencedor: {vencedor}")
            return turno, vencedor

        if jogo.jogador_atual == Jogador.JOGADOR1:
            ia_j1.fazer_movimento()
        else:
            ia_j2.fazer_movimento()

    print("Empate por limite de turnos.")
    return 200, None

simular_partida()
```

---

**Próximo:** [Pontos de Atenção](pontos-atencao.md)
