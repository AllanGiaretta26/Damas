"""
Módulo de serviços do jogo de damas.
Exporta todas as classes de serviço.
"""

from src.services.movimento_validator import MovimentoValidator
from src.services.capture_handler import CaptureHandler
from src.services.promotion_handler import PromotionHandler

__all__ = [
    'MovimentoValidator',
    'CaptureHandler',
    'PromotionHandler',
]
