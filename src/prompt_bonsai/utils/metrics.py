"""Metrics and analytics for prompt-bonsai."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class CompressionMetrics:
    """Metrics for a single compression operation."""
    original_tokens: int
    compressed_tokens: int
    target_ratio: float
    achieved_ratio: float
    quality_score: float
    strategy_used: str
    duration_ms: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)

    @property
    def token_savings(self) -> int:
        """Number of tokens saved."""
        return self.original_tokens - self.compressed_tokens

    @property
    def savings_percentage(self) -> float:
        """Percentage of tokens saved."""
        if self.original_tokens == 0:
            return 0.0
        return (self.token_savings / self.original_tokens) * 100

    @property
    def cost_savings_usd(self, price_per_1k_tokens: float = 0.01) -> float:
        """Estimated cost savings in USD (default: $0.01 per 1K tokens)."""
        return (self.token_savings / 1000) * price_per_1k_tokens


class MetricsCollector:
    """Collect and aggregate compression metrics."""

    def __init__(self) -> None:
        self._metrics: List[CompressionMetrics] = []

    def record(self, metric: CompressionMetrics) -> None:
        """Record a compression metric."""
        self._metrics.append(metric)

    def summary(self) -> Dict:
        """Get summary statistics."""
        if not self._metrics:
            return {}

        total_original = sum(m.original_tokens for m in self._metrics)
        total_compressed = sum(m.compressed_tokens for m in self._metrics)
        avg_quality = sum(m.quality_score for m in self._metrics) / len(self._metrics)
        avg_ratio = sum(m.achieved_ratio for m in self._metrics) / len(self._metrics)

        return {
            "total_compressions": len(self._metrics),
            "total_tokens_saved": total_original - total_compressed,
            "avg_savings_percentage": ((total_original - total_compressed) / total_original) * 100,
            "avg_quality_score": avg_quality,
            "avg_compression_ratio": avg_ratio,
            "total_estimated_savings_usd": sum(
                m.cost_savings_usd for m in self._metrics
            ),
        }

    def reset(self) -> None:
        """Clear all metrics."""
        self._metrics = []
