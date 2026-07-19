"""High-level compressor API for prompt-bonsai."""

from typing import Optional, List, Union

from prompt_bonsai.config import CompressionConfig, CompressionStrategy
from prompt_bonsai.compressors.base import CompressionResult
from prompt_bonsai.compressors.semantic import SemanticCompressor
from prompt_bonsai.compressors.structural import StructuralCompressor
from prompt_bonsai.compressors.hybrid import HybridCompressor
from prompt_bonsai.exceptions import StrategyError
from prompt_bonsai.utils.metrics import MetricsCollector, CompressionMetrics


class Compressor:
    """Main compressor class — the primary user-facing API.

    Usage:
        >>> from prompt_bonsai import Compressor
        >>> compressor = Compressor(strategy="hybrid", target_ratio=0.3)
        >>> result = compressor.compress("Your long prompt here...")
        >>> print(result.text)
        >>> print(f"Saved {result.original_tokens - result.compressed_tokens} tokens")

    Args:
        strategy: Compression strategy ("semantic", "structural", "hybrid").
        target_ratio: Target compression ratio (0.0-1.0).
        min_quality: Minimum quality threshold (0.0-1.0).
        preserve: List of strings/patterns to preserve during compression.
        config: Full CompressionConfig object (overrides other args).
        model_name: Model name for tokenizer (e.g., "gpt-4", "claude-3").
        verbose: Whether to print compression details.
    """

    _STRATEGY_MAP = {
        CompressionStrategy.SEMANTIC: SemanticCompressor,
        CompressionStrategy.STRUCTURAL: StructuralCompressor,
        CompressionStrategy.HYBRID: HybridCompressor,
        "semantic": SemanticCompressor,
        "structural": StructuralCompressor,
        "hybrid": HybridCompressor,
    }

    def __init__(
        self,
        strategy: Union[str, CompressionStrategy] = "hybrid",
        target_ratio: float = 0.3,
        min_quality: float = 0.70,
        preserve: Optional[List[str]] = None,
        config: Optional[CompressionConfig] = None,
        model_name: Optional[str] = None,
        verbose: bool = False,
    ) -> None:
        self.config = config or CompressionConfig(
            strategy=CompressionStrategy(strategy) if isinstance(strategy, str) else strategy,
            target_ratio=target_ratio,
            min_quality=min_quality,
            preserve_patterns=preserve or [],
            model_name=model_name,
            verbose=verbose,
        )

        self._compressor = self._create_compressor()
        self._metrics = MetricsCollector()
        self.verbose = verbose

    def _create_compressor(self):
        """Create the appropriate compressor instance."""
        strategy = self.config.strategy
        compressor_class = self._STRATEGY_MAP.get(strategy)

        if compressor_class is None:
            valid = list(self._STRATEGY_MAP.keys())
            raise StrategyError(
                f"Unknown strategy: {strategy}. Valid options: {valid}"
            )

        return compressor_class(self.config)

    def compress(
        self,
        text: str,
        target_ratio: Optional[float] = None,
        preserve: Optional[List[str]] = None,
    ) -> CompressionResult:
        """Compress a prompt.

        Args:
            text: The prompt text to compress.
            target_ratio: Override target ratio for this call.
            preserve: Additional patterns to preserve for this call.

        Returns:
            CompressionResult with compressed text and metadata.
        """
        preserve_patterns = list(self.config.preserve_patterns)
        if preserve:
            preserve_patterns.extend(preserve)

        result = self._compressor.compress(text, target_ratio, preserve_patterns)

        # Record metrics
        metric = CompressionMetrics(
            original_tokens=result.original_tokens,
            compressed_tokens=result.compressed_tokens,
            target_ratio=target_ratio or self.config.target_ratio,
            achieved_ratio=result.compressed_tokens / max(result.original_tokens, 1),
            quality_score=result.quality_report.overall_score,
            strategy_used=result.strategy,
            duration_ms=result.metadata.get("duration_ms", 0.0),
            metadata=result.metadata,
        )
        self._metrics.record(metric)

        if self.verbose:
            self._print_result(result)

        return result

    def estimate(self, text: str) -> int:
        """Estimate token count for text."""
        return self._compressor.estimate_tokens(text)

    def stats(self) -> dict:
        """Get compression statistics."""
        return self._metrics.summary()

    def reset_stats(self) -> None:
        """Reset compression statistics."""
        self._metrics.reset()

    def _print_result(self, result: CompressionResult) -> None:
        """Print compression result details."""
        from rich.console import Console
        from rich.table import Table

        console = Console()

        table = Table(title="Prompt Bonsai Compression Result")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Strategy", result.strategy)
        table.add_row("Original Tokens", str(result.original_tokens))
        table.add_row("Compressed Tokens", str(result.compressed_tokens))
        table.add_row(
            "Tokens Saved",
            f"{result.original_tokens - result.compressed_tokens} "
            f"({((result.original_tokens - result.compressed_tokens) / max(result.original_tokens, 1) * 100):.1f}%)"
        )
        table.add_row("Quality Score", f"{result.quality_report.overall_score:.3f}")
        table.add_row("Semantic Similarity", f"{result.quality_report.semantic_similarity:.3f}")
        table.add_row("Structural Integrity", f"{result.quality_report.structural_integrity:.3f}")

        if result.quality_report.warnings:
            table.add_row("Warnings", "\n".join(result.quality_report.warnings))

        console.print(table)


# Convenience function for one-off compression
def compress(
    text: str,
    ratio: float = 0.3,
    strategy: str = "hybrid",
    preserve: Optional[List[str]] = None,
    min_quality: float = 0.70,
    model_name: Optional[str] = None,
) -> str:
    """One-shot prompt compression.

    This is the simplest way to compress a prompt:

        >>> from prompt_bonsai import compress
        >>> short = compress("Your very long prompt here...", ratio=0.3)

    Args:
        text: The prompt text to compress.
        ratio: Target compression ratio (0.0-1.0).
        strategy: Compression strategy ("semantic", "structural", "hybrid").
        preserve: Patterns to preserve during compression.
        min_quality: Minimum quality threshold.
        model_name: Model name for tokenizer.

    Returns:
        Compressed prompt text.
    """
    compressor = Compressor(
        strategy=strategy,
        target_ratio=ratio,
        min_quality=min_quality,
        preserve=preserve,
        model_name=model_name,
    )
    result = compressor.compress(text)
    return result.text
