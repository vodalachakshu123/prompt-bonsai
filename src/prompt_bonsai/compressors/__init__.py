"""Compressor implementations for prompt-bonsai."""

from prompt_bonsai.compressors.base import BaseCompressor, CompressionResult
from prompt_bonsai.compressors.semantic import SemanticCompressor
from prompt_bonsai.compressors.structural import StructuralCompressor
from prompt_bonsai.compressors.hybrid import HybridCompressor

__all__ = [
    "BaseCompressor",
    "CompressionResult",
    "SemanticCompressor",
    "StructuralCompressor",
    "HybridCompressor",
]
