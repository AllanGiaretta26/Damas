"""
Arquivo de configuração do Jogo de Damas

Use este arquivo para personalizar cores, tamanhos e outras propriedades da interface.
Ele é importado pela interface gráfica (gui.py).
"""

# Configurações de Tabuleiro
TAMANHO_TABULEIRO = 8
TAMANHO_CASA_PIXELS = 80

# Cores do Tabuleiro
COR_CASA_BRANCA = "#FFD700"      # Ouro claro
COR_CASA_PRETA = "#000000"       # Preto
COR_FUNDO_TABULEIRO = "#CCCCCC"  # Cinza

# Cores de Destaque
COR_SELECIONADA = "#FF6B6B"      # Vermelho claro
COR_MOVIMENTO_VALIDO = "#90EE90" # Verde claro
COR_CAPTURA = "#FFA500"          # Laranja

# Cores das Peças
COR_PECA_JOGADOR1 = "#FF0000"    # Vermelho
COR_PECA_JOGADOR2 = "#0000FF"    # Azul
COR_DAMA = "#FFD700"             # Ouro (coroa da dama)

# Configurações de Texto
FONTE_TITULO = ("Arial", 18, "bold")
FONTE_INFO = ("Arial", 12)
FONTE_PEQUENA = ("Arial", 10)

# Configurações de Botões
COR_BOTAO_NOVO = "#FF6B6B"      # Vermelho claro
COR_BOTAO_NOVO_HOVER = "#FF5555" # Vermelho mais escuro

COR_BOTAO_IA = "#4A90E2"         # Azul
COR_BOTAO_IA_HOVER = "#3A7FD7"   # Azul mais escuro

COR_BOTAO_PADRAO = "#CCCCCC"     # Cinza

# Configurações de IA
DELAY_IA_MILISEGUNDOS = 500      # Tempo antes da IA fazer movimento
DIFICULDADE_IA = "normal"        # "fácil", "normal", "difícil"

# Configurações de Som (futuro)
HABILITAR_SONS = False
VOLUME_SONS = 0.7

# Configurações de Jogo
VELOCIDADE_ANIMACAO = 100        # Milisegundos
MOSTRAR_HISTORICO = True
CONTAR_REMOVIDAS = True

# Exemplos de temas alternativos
# Descomente a linha abaixo para usar um tema alternativo

# TEMA_ESCURO = {
#     "COR_CASA_BRANCA": "#333333",
#     "COR_CASA_PRETA": "#555555",
#     "COR_FUNDO_TABULEIRO": "#222222",
#     "COR_PECA_JOGADOR1": "#FF6B6B",
#     "COR_PECA_JOGADOR2": "#6B9FFF",
# }

# TEMA_NATURAL = {
#     "COR_CASA_BRANCA": "#F5D5B8",
#     "COR_CASA_PRETA": "#8B4513",
#     "COR_FUNDO_TABULEIRO": "#D2B48C",
#     "COR_PECA_JOGADOR1": "#8B0000",
#     "COR_PECA_JOGADOR2": "#001F4D",
# }


def aplicar_tema(tema_nome: str = "padrao"):
    """
    Aplica um tema pré-definido ao jogo.
    
    Args:
        tema_nome: Nome do tema ("padrao", "escuro", "natural")
    """
    global COR_CASA_BRANCA, COR_CASA_PRETA, COR_FUNDO_TABULEIRO
    global COR_PECA_JOGADOR1, COR_PECA_JOGADOR2
    
    temas = {
        "padrao": {
            "COR_CASA_BRANCA": "#FFD700",
            "COR_CASA_PRETA": "#000000",
            "COR_FUNDO_TABULEIRO": "#CCCCCC",
            "COR_PECA_JOGADOR1": "#FF0000",
            "COR_PECA_JOGADOR2": "#0000FF",
        },
        "escuro": {
            "COR_CASA_BRANCA": "#333333",
            "COR_CASA_PRETA": "#555555",
            "COR_FUNDO_TABULEIRO": "#222222",
            "COR_PECA_JOGADOR1": "#FF6B6B",
            "COR_PECA_JOGADOR2": "#6B9FFF",
        },
        "natural": {
            "COR_CASA_BRANCA": "#F5D5B8",
            "COR_CASA_PRETA": "#8B4513",
            "COR_FUNDO_TABULEIRO": "#D2B48C",
            "COR_PECA_JOGADOR1": "#8B0000",
            "COR_PECA_JOGADOR2": "#001F4D",
        }
    }
    
    if tema_nome in temas:
        tema = temas[tema_nome]
        COR_CASA_BRANCA = tema["COR_CASA_BRANCA"]
        COR_CASA_PRETA = tema["COR_CASA_PRETA"]
        COR_FUNDO_TABULEIRO = tema["COR_FUNDO_TABULEIRO"]
        COR_PECA_JOGADOR1 = tema["COR_PECA_JOGADOR1"]
        COR_PECA_JOGADOR2 = tema["COR_PECA_JOGADOR2"]
