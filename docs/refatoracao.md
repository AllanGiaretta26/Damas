# Refatoração do Jogo de Damas - Aplicação dos Princípios SOLID e Clean Code

## Visão Geral

Este documento descreve as mudanças aplicadas ao projeto do Jogo de Damas para melhorar a manutenibilidade, testabilidade e extensibilidade do código, seguindo os princípios SOLID e as práticas de Clean Code.

---

## Estrutura do Projeto (Antes vs Depois)

### Antes
```
src/
├── game.py       # Toda lógica do jogo em uma classe
├── gui.py        # Interface gráfica monolítica
├── ia.py         # IA com lógica fixa
└── config.py     # Configurações
```

### Depois
```
src/
├── models/                   # Classes de domínio (SRP)
│   ├── __init__.py
│   ├── enums.py             # Enumerações (Jogador, TipoPeca, CorPeca)
│   ├── peca.py              # Classe Peca
│   └── tabuleiro.py         # Classe Tabuleiro
├── services/                 # Serviços especializados (SRP)
│   ├── __init__.py
│   ├── movimento_validator.py   # Validação de movimentos
│   ├── capture_handler.py       # Gerenciamento de capturas
│   └── promotion_handler.py     # Promoção de peças
├── ia/                       # IA com Strategy Pattern (OCP/DIP)
│   ├── __init__.py
│   └── estrategias.py        # Estratégias por dificuldade
├── gui/                      # GUI separada em responsabilidades (SRP)
│   ├── __init__.py
│   ├── renderizador.py          # Renderização de elementos
│   └── gerenciador_interface.py # Gerenciamento de UI e eventos
├── game.py                   # Classe Jogo (orquestradora)
└── config.py                 # Configurações melhor organizadas
```

---

## Princípios SOLID Aplicados

### 1. Single Responsibility Principle (SRP)

**Problema anterior:** A classe `Jogo` fazia tudo: validava movimentos, executava capturas, promovia peças, gerenciava turno, etc.

**Solução:**
- **`MovimentoValidator`**: Responsável apenas por validar e calcular movimentos
- **`CaptureHandler`**: Responsável apenas por executar e gerenciar capturas
- **`PromotionHandler`**: Responsável apenas por promover peças
- **`RenderizadorTabuleiro`**: Responsável apenas por desenhar na tela
- **`GerenciadorInterface`**: Responsável apenas por gerenciar eventos e elementos UI
- **`Jogo`**: Agora é uma classe orquestradora que delega responsabilidades aos serviços

### 2. Open/Closed Principle (OCP)

**Problema anterior:** Para adicionar novos níveis de dificuldade à IA, era necessário modificar a classe `IA`.

**Solução:**
- Criada interface `EstrategiaIA` (classe abstrata)
- Implementadas estratégias: `EstrategiaFacil`, `EstrategiaNormal`, `EstrategiaDificil`
- Para adicionar nova dificuldade: criar nova classe que estende `EstrategiaIA` sem modificar código existente

```python
class EstrategiaMuitoDificil(EstrategiaIA):
    def escolher_movimento(self, jogo, movimentos):
        # Implementar nova estratégia
        pass
```

### 3. Liskov Substitution Principle (LSP)

**Aplicação:** Todas as classes de estratégia herdam de `EstrategiaIA` e podem ser substituídas entre si sem quebrar o comportamento da classe `IA`.

### 4. Interface Segregation Principle (ISP)

**Aplicação:** Cada serviço tem interface específica com apenas os métodos necessários:
- `MovimentoValidator`: focado em validação
- `CaptureHandler`: focado em capturas
- `PromotionHandler`: focado em promoções

### 5. Dependency Inversion Principle (DIP)

**Problema anterior:** A classe `Jogo` dependia de implementações concretas embutidas.

**Solução:**
- `Jogo` agora depende de serviços injetados
- `IA` depende da abstração `EstrategiaIA`, não de implementações concretas
- Factory method `_criar_estrategia()` cria instâncias conforme necessidade

---

## Clean Code Aplicado

### Nomes Significativos
- `em_sequencia_captura` ao invés de nomes genéricos
- `pecas_capturadas_jogador1` ao invés de `piezas_capturadas_j1`
- Métodos como `calcular_movimentos_validos()`, `executar_captura()`

### Métodos Pequenos e Focados
- Cada método faz uma coisa e faz bem feito
- Exemplo: `_registrar_captura()`, `_registrar_jogada()`, `_encerrar_turno()`

### Properties ao Invés de Acesso Direto
```python
@property
def movimentos_validos(self) -> List[Tuple[int, int]]:
    return self._movimentos_validos

@movimentos_validos.setter
def movimentos_validos(self, movimentos: List[Tuple[int, int]]) -> None:
    self._movimentos_validos = movimentos
```

### Docstrings Completas
Todas as classes e métodos públicos possuem docstrings explicando:
- Responsabilidade
- Parâmetros
- Retorno
- Exceções

### Código DRY (Don't Repeat Yourself)
- Lógica de validação centralizada em `MovimentoValidator`
- Lógica de renderização centralizada em `RenderizadorTabuleiro`
- Configurações agrupadas e documentadas em `config.py`

---

## Melhorias na Testabilidade

### Testes Isolados
- Serviços podem ser testados independentemente
- Mocking facilitado por uso de interfaces

### Métodos Públicos para Testes
```python
jogo.obter_movimentos_validos_para_peca(linha, coluna)
jogo.jogador_tem_capturas(jogador)
jogo.encontrar_capturas_para_peca(linha, coluna)
```

---

## Benefícios da Refatoração

1. **Manutenibilidade**: Mudanças são mais fááceis de localizar e implementar
2. **Testabilidade**: Cada componente pode ser testado isoladamente
3. **Extensibilidade**: Novas funcionalidades são adicionadas sem modificar código existente
4. **Legibilidade**: Código é mais fácil de entender e navegar
5. **Reusabilidade**: Serviços podem ser reutilizados em outros contextos
6. **Separação de Preocupações**: UI, lógica de jogo e serviços estão separados

---

## Como Executar

```bash
# Executar testes
python teste_jogo.py

# Iniciar jogo
python main.py
```

---

## Padrões de Projeto Utilizados

| Padrão | Localização | Propósito |
|--------|-------------|-----------|
| Strategy | `src/ia/estrategias.py` | Permitir diferentes níveis de dificuldade |
| Factory Method | `src/ia/__init__.py` | Criar estratégias conforme dificuldade |
| Facade | `src/gui/__init__.py` | Simplificar acesso à GUI |
| Dependency Injection | `src/game.py` | Injetar serviços na classe Jogo |
| Service Layer | `src/services/` | Encapsular lógica de negócio especializada |

---

## Conclusão

A refatoração aplicou consistentemente os princípios SOLID e práticas de Clean Code, resultando em um código mais limpo, testável e mantível. A estrutura modular permite fácil extensão e manutenção futura.
