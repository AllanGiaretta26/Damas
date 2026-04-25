"""
Arquivo de configuração do Jogo de Damas

Use este arquivo para personalizar cores, tamanhos e outras propriedades da interface.
Ele é importado pela interface gráfica (gui.py).
"""

# ============================================================
# CONFIGURAÇÕES DE TABULEIRO
# ============================================================
TAMANHO_TABULEIRO = 8
TAMANHO_CASA_PIXELS = 80
TAMANHO_COORDENADAS_PIXELS = 20

# ============================================================
# CORES DO TABULEIRO
# ============================================================
COR_CASA_BRANCA = "#F0D9B5"      # Creme claro (clássico xadrez)
COR_CASA_PRETA = "#B58863"       # Marrom (clássico xadrez)
COR_FUNDO_TABULEIRO = "#2C3E50"  # Azul-escuro (UI moderna)

# ============================================================
# CORES DE DESTAQUE
# ============================================================
COR_SELECIONADA = "#829769"      # Verde-oliva
COR_MOVIMENTO_VALIDO = "#CDD26A" # Amarelo-verde sutil
COR_CAPTURA = "#E05C40"          # Laranja-vermelho

# ============================================================
# CORES DAS PEÇAS
# ============================================================
COR_PECA_JOGADOR1 = "#E74C3C"    # Vermelho vivo
COR_PECA_JOGADOR2 = "#3498DB"    # Azul suave
COR_DAMA = "#F1C40F"             # Ouro vivo (coroa da dama)

# ============================================================
# CONFIGURAÇÕES DE TEXTO
# ============================================================
FONTE_TITULO = ("Arial", 18, "bold")
FONTE_INFO = ("Arial", 12)
FONTE_PEQUENA = ("Arial", 10)

# Cores de texto sobre fundo escuro
COR_TEXTO_PRINCIPAL = "#ECF0F1"
COR_TEXTO_SECUNDARIO = "#BDC3C7"

# ============================================================
# CONFIGURAÇÕES DE BOTÕES
# ============================================================
COR_BOTAO_NOVO = "#E74C3C"       # Vermelho (Novo Jogo)
COR_BOTAO_NOVO_HOVER = "#C0392B"

COR_BOTAO_IA = "#3498DB"         # Azul (Contra IA)
COR_BOTAO_IA_HOVER = "#2980B9"

COR_BOTAO_PADRAO = "#34495E"     # Cinza-escuro (botões neutros)
COR_BOTAO_PADRAO_HOVER = "#2C3E50"

COR_BOTAO_EMPATE = "#D35400"     # Laranja-escuro (Empate)
COR_BOTAO_EMPATE_HOVER = "#A04000"

# ============================================================
# CONFIGURAÇÕES DE IA
# ============================================================
DELAY_IA_MILISEGUNDOS = 500      # Tempo antes da IA fazer movimento
DIFICULDADE_IA = "normal"        # "fácil", "normal", "difícil"

# ============================================================
# CONFIGURAÇÕES DE SOM (futuro)
# ============================================================
HABILITAR_SONS = False
VOLUME_SONS = 0.7

# ============================================================
# CONFIGURAÇÕES DE JOGO
# ============================================================
VELOCIDADE_ANIMACAO = 100        # Milisegundos
MOSTRAR_HISTORICO = True
CONTAR_REMOVIDAS = True


# ============================================================
# TEMAS ALTERNATIVOS
# ============================================================

TEMA_ESCURO = {
    "COR_CASA_BRANCA": "#333333",
    "COR_CASA_PRETA": "#555555",
    "COR_FUNDO_TABULEIRO": "#1A1A2E",
    "COR_PECA_JOGADOR1": "#E74C3C",
    "COR_PECA_JOGADOR2": "#3498DB",
}

TEMA_NATURAL = {
    "COR_CASA_BRANCA": "#F5D5B8",
    "COR_CASA_PRETA": "#8B4513",
    "COR_FUNDO_TABULEIRO": "#D2B48C",
    "COR_PECA_JOGADOR1": "#8B0000",
    "COR_PECA_JOGADOR2": "#001F4D",
}


def aplicar_tema(tema_nome: str = "padrao") -> dict:
    """
    Aplica um tema pré-definido ao jogo.
    
    Args:
        tema_nome: Nome do tema ("padrao", "escuro", "natural")
        
    Returns:
        Dicionário com as configurações do tema
    """
    temas = {
        "padrao": {
            "COR_CASA_BRANCA": "#FFD700",
            "COR_CASA_PRETA": "#000000",
            "COR_FUNDO_TABULEIRO": "#CCCCCC",
            "COR_PECA_JOGADOR1": "#FF0000",
            "COR_PECA_JOGADOR2": "#0000FF",
        },
        "escuro": TEMA_ESCURO,
        "natural": TEMA_NATURAL,
    }

    if tema_nome not in temas:
        raise ValueError(f"Tema '{tema_nome}' não encontrado. Temas disponíveis: {list(temas.keys())}")

    return temas[tema_nome]


def obter_todas_cores() -> dict:
    """
    Retorna todas as configurações de cores atuais.
    
    Returns:
        Dicionário com todas as configurações de cores
    """
    return {
        "COR_CASA_BRANCA": COR_CASA_BRANCA,
        "COR_CASA_PRETA": COR_CASA_PRETA,
        "COR_FUNDO_TABULEIRO": COR_FUNDO_TABULEIRO,
        "COR_SELECIONADA": COR_SELECIONADA,
        "COR_MOVIMENTO_VALIDO": COR_MOVIMENTO_VALIDO,
        "COR_CAPTURA": COR_CAPTURA,
        "COR_PECA_JOGADOR1": COR_PECA_JOGADOR1,
        "COR_PECA_JOGADOR2": COR_PECA_JOGADOR2,
        "COR_DAMA": COR_DAMA,
    }
