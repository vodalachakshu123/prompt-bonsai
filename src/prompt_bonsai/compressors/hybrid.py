"""Hybrid compression strategy.

Combines semantic and structural compression intelligently,
applying the best strategy based on prompt content analysis.
"""

import re
from typing import Optional, List, Dict

from prompt_bonsai.compressors.base import BaseCompressor, CompressionResult
from prompt_bonsai.compressors.semantic import SemanticCompressor
from prompt_bonsai.compressors.structural import StructuralCompressor
from prompt_bonsai.config import CompressionConfig
from prompt_bonsai.exceptions import CompressionError


class HybridCompressor(BaseCompressor):
    """Intelligent hybrid compressor that selects the best strategy."""

    def __init__(self, config: Optional[CompressionConfig] = None) -> None:
        super().__init__(config)
        self.semantic = SemanticCompressor(config)
        self.structural = StructuralCompressor(config)
        self._last_iterations = 1

    def _compress_impl(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]] = None,
    ) -> str:
        """Compress using hybrid strategy."""
        # Analyze prompt type
        prompt_type = self._analyze_prompt_type(text)

        if prompt_type == "structured":
            # For structured prompts (JSON, XML, code), structural first
            compressed = self._structural_then_semantic(
                text, target_tokens, preserve_patterns
            )
        elif prompt_type == "conversational":
            # For conversational prompts, semantic first
            compressed = self._semantic_then_structural(
                text, target_tokens, preserve_patterns
            )
        else:
            # For mixed content, interleave both
            compressed = self._interleaved(
                text, target_tokens, preserve_patterns
            )

        return compressed

    def _analyze_prompt_type(self, text: str) -> str:
        """Analyze prompt to determine best compression approach.

        Returns: 'structured', 'conversational', or 'mixed'
        """
        scores = {
            "structured": 0,
            "conversational": 0,
        }

        # Structured indicators
        if re.search(r'\{[\s\S]*\}', text):
            scores["structured"] += 2
        if re.search(r'<[^>]+>', text):
            scores["structured"] += 2
        if re.search(r'```\w*\n', text):
            scores["structured"] += 2
        if re.search(r'\[\s*\{', text):
            scores["structured"] += 1

        # Conversational indicators
        if re.search(r'\b(hello|hi|hey|please|thank|thanks)\b', text, re.I):
            scores["conversational"] += 1
        if re.search(r'\b(I am|I\'m|I would|could you|would you)\b', text, re.I):
            scores["conversational"] += 1
        if text.count('?') > 0:
            scores["conversational"] += 1
        if len(text.split('\n\n')) <= 2 and len(text) < 500:
            scores["conversational"] += 1

        if scores["structured"] > scores["conversational"]:
            return "structured"
        elif scores["conversational"] > scores["structured"]:
            return "conversational"
        else:
            return "mixed"

    def _structural_then_semantic(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]],
    ) -> str:
        """Apply structural then semantic compression."""
        # Phase 1: Structural
        compressed = self.structural._compress_impl(text, target_tokens, preserve_patterns)

        # Phase 2: Semantic if still over target
        if self.tokenizer.count(compressed) > target_tokens:
            compressed = self.semantic._compress_impl(
                compressed, target_tokens, preserve_patterns
            )

        return compressed

    def _semantic_then_structural(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]],
    ) -> str:
        """Apply semantic then structural compression."""
        # Phase 1: Semantic
        compressed = self.semantic._compress_impl(text, target_tokens, preserve_patterns)

        # Phase 2: Structural if still over target
        if self.tokenizer.count(compressed) > target_tokens:
            compressed = self.structural._compress_impl(
                compressed, target_tokens, preserve_patterns
            )

        return compressed

    def _interleaved(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]],
    ) -> str:
        """Apply both strategies in alternating passes."""
        compressed = text
        iteration = 0
        max_iter = self.config.max_iterations

        while (
            self.tokenizer.count(compressed) > target_tokens
            and iteration < max_iter
        ):
            iteration += 1

            if iteration % 2 == 1:
                compressed = self.semantic._compress_impl(
                    compressed, target_tokens, preserve_patterns
                )
            else:
                compressed = self.structural._compress_impl(
                    compressed, target_tokens, preserve_patterns
                )

            if self.tokenizer.count(compressed) <= target_tokens:
                break

        self._last_iterations = iteration
        return compressed

    def compress(self, text: str, target_ratio: Optional[float] = None,
                 preserve_patterns: Optional[List[str]] = None) -> CompressionResult:
        """Override compress to include prompt type in metadata."""
        result = super().compress(text, target_ratio, preserve_patterns)
        result.metadata["prompt_type"] = self._analyze_prompt_type(text)
        return result
