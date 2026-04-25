# 📚 Documentação: Jogo de Damas em Python

## Visão Geral Rápida

**Jogo de damas interativo** com interface gráfica (tkinter) e IA com 3 níveis de dificuldade.

- 🎮 Interface 8×8 com clique para mover
- 🤖 IA: Fácil (aleatório), Normal (heurística), Difícil (minimax)
- ♟️ Regras completas: captura obrigatória, promoção, sequência
- 📊 Desfazer jogadas (útil com IA)
- 🎨 Temas e cores configuráveis

**Tecnologia:** Python 3.7+ | tkinter | Arquitetura limpa em camadas

---

## 📖 Índice de Documentos

### 1. [Arquitetura](arquitetura.md)
- Estrutura de pastas
- Padrão de dependências
- Fluxo de dados

### 2. [Models (Dados)](models.md)
- Enums: `TipoPeca`, `Jogador`, `CorPeca`
- Classe `Peca` (posição, tipo, promoção)
- Classe `Tabuleiro` (8×8, acesso às peças)

### 3. [Services (Regras)](services.md)
- `MovimentoValidator` — valida movimentos legais
- `CaptureHandler` — executa capturas e sequências
- `PromotionHandler` — promove peças a dama

### 4. [Game (Orquestrador)](game.md)
- Classe `Jogo` — maestro central
- Fluxo de movimento
- Sistema de histórico e undo

### 5. [IA (Inteligência Artificial)](ia.md)
- `EstrategiaFacil` — aleatória
- `EstrategiaNormal` — heurística com prioridades
- `EstrategiaMedia` — minimax profundidade 3
- `EstrategiaDificil` — minimax profundidade 5 (base: `EstrategiaMinimax`)

### 6. [GUI (Interface)](gui.md)
- `Renderizador` — desenha o tabuleiro
- `GerenciadorInterface` — lida com cliques
- `GUIJogo` — widget principal
- Integração com IA

### 7. [Main & Aplicação](main.md)
- `AplicacaoDamas` — gerencia ciclo de vida
- Menu, opções, fluxo de jogo

### 8. [Exemplos de Uso](uso-exemplo.md)
- Como usar a classe `Jogo`
- Como integrar a IA
- Exemplos de testes

### 9. [Pontos de Atenção](pontos-atencao.md)
- Erros comuns e como evitar
- Comportamentos importantes
- Performance e otimizações
- O que quebra testes

---

## 🚀 Início Rápido

### Executar o jogo
```bash
python main.py
```

### Executar testes
```bash
python tests/teste_jogo.py
```

### Estrutura de código
```
src/
├── models/        ← Dados puros (Peca, Tabuleiro, Enums)
├── services/      ← Regras (Movimento, Captura, Promoção)
├── game.py        ← Orquestrador (Jogo)
├── ia/            ← IA (Estratégias)
├── gui/           ← Interface (GUI, Renderizador)
└── config.py      ← Configurações visuais
```

---

## 🔗 Links Importantes

- **Testes:** [teste_jogo.py](../tests/teste_jogo.py)
- **Config:** [config.py](../src/config.py)
- **Main:** [main.py](../main.py)

---

## 📝 Notas

- Todos os identificadores estão em **português (pt-BR)**
- Sem dependências externas (só stdlib + tkinter)
- Testes são scripts procedurais (não unittest)
- Arquitetura em camadas com padrões SOLID

