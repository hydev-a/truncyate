"""
Truncayte - Precision Truncator: A smart text truncation tool for RAG systems and LLMs.
Preserves context while reducing text to desired lengths.
"""

from .truncator import PrecisionTruncator, TruncationStrategy
from .utils import count_tokens, extract_key_sentences
from .cli import main

__version__ = "0.1.0"
__all__ = ["PrecisionTruncator", "TruncationStrategy", "count_tokens", "extract_key_sentences", "main"]