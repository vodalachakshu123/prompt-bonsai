"""Base compressor interface."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from prompt_bonsai.config import CompressionConfig
from prompt_bonsai.utils.tokenizer import Tokenizer
from prompt_bonsai.utils.quality import QualityAssessor, QualityReport
from prompt_bonsai.utils.metrics import CompressionMetrics
from prompt_bonsai.exceptions import CompressionError, QualityError


@dataclass
class CompressionResult:
    """Result of a compression operation."""
    text: str
    original_tokens: int
    compressed_tokens: int
    quality_report: QualityReport
    strategy: str
    metadata: Dict[str, Any]


class BaseCompressor(ABC):
    """Abstract base class for all compressors."""

    def __init__(self, config: Optional[CompressionConfig] = None) -> None:
        self.config = config or CompressionConfig()
        self.tokenizer = Tokenizer(
            backend=self.config.tokenizer_backend,
            model_name=self.config.model_name,
        )
        self.quality_assessor = QualityAssessor()

    @abstractmethod
    def _compress_impl(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]] = None,
    ) -> str:
        """Implementation of compression logic."""
        pass

    def compress(
        self,
        text: str,
        target_ratio: Optional[float] = None,
        preserve_patterns: Optional[List[str]] = None,
    ) -> CompressionResult:
        """Compress a prompt.

        Args:
            text: The prompt text to compress.
            target_ratio: Target compression ratio (overrides config).
            preserve_patterns: Patterns to preserve (overrides config).

        Returns:
            CompressionResult with compressed text and metadata.
        """
        import time

        ratio = target_ratio or self.config.target_ratio
        patterns = preserve_patterns or self.config.preserve_patterns

        original_tokens = self.tokenizer.count(text)
        target_tokens = int(original_tokens * (1 - ratio))

        if target_tokens >= original_tokens:
            # Nothing to compress
            quality = self.quality_assessor.assess(text, text, patterns)
            return CompressionResult(
                text=text,
                original_tokens=original_tokens,
                compressed_tokens=original_tokens,
                quality_report=quality,
                strategy=self.__class__.__name__,
                metadata={"skipped": True, "reason": "target_ratio too low"},
            )

        start_time = time.perf_counter()

        try:
            compressed = self._compress_impl(text, target_tokens, patterns)
        except Exception as e:
            raise CompressionError(f"Compression failed: {e}") from e

        duration_ms = (time.perf_counter() - start_time) * 1000
        compressed_tokens = self.tokenizer.count(compressed)

        # Quality check
        quality = self.quality_assessor.assess(text, compressed, patterns)

        if quality.overall_score < self.config.min_quality:
            raise QualityError(
                f"Compressed prompt quality ({quality.overall_score:.2f}) "
                f"below minimum threshold ({self.config.min_quality})"
            )

        return CompressionResult(
            text=compressed,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            quality_report=quality,
            strategy=self.__class__.__name__,
            metadata={
                "duration_ms": duration_ms,
                "target_tokens": target_tokens,
                "iterations": getattr(self, "_last_iterations", 1),
            },
        )

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return self.tokenizer.count(text)
