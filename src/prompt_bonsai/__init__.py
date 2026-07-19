"""
Prompt Bonsai — Intelligent prompt compression for LLMs.

Cut your token costs by 30-70% without losing meaning.

Basic usage:
    >>> from prompt_bonsai import compress, Compressor
    >>> compressed = compress("Your very long prompt here...", ratio=0.5)
    >>> print(compressed)

Advanced usage:
    >>> compressor = Compressor(strategy="semantic", min_quality=0.95)
    >>> result = compressor.compress(prompt, preserve=["{user_input}"])
"""

from prompt_bonsai._version import __version__
from prompt_bonsai.compressor import Compressor, compress
from prompt_bonsai.config import CompressionConfig
from prompt_bonsai.exceptions import (
    CompressionError,
    QualityError,
    TokenizationError,
    StrategyError,
)

__all__ = [
    "__version__",
    "Compressor",
    "compress",
    "CompressionConfig",
    "CompressionError",
    "QualityError",
    "TokenizationError",
    "StrategyError",
]
