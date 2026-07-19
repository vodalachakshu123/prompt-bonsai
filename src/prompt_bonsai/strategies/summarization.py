"""Extractive summarization strategy for long prompts."""

from typing import Optional, List

from prompt_bonsai.compressors.base import BaseCompressor
from prompt_bonsai.config import CompressionConfig


class SummarizationCompressor(BaseCompressor):
    """Compress by extractive summarization of long text sections."""

    def __init__(self, config: Optional[CompressionConfig] = None) -> None:
        super().__init__(config)
        self._last_iterations = 1

    def _compress_impl(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]] = None,
    ) -> str:
        """Compress using extractive summarization.

        This is a placeholder for future implementation that would use
        sentence scoring and selection to create summaries.
        """
        # For now, fall back to semantic compression
        from prompt_bonsai.compressors.semantic import SemanticCompressor
        fallback = SemanticCompressor(self.config)
        return fallback._compress_impl(text, target_tokens, preserve_patterns)
