"""Configuration classes for prompt-bonsai."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class CompressionStrategy(str, Enum):
    """Available compression strategies."""
    SEMANTIC = "semantic"
    STRUCTURAL = "structural"
    HYBRID = "hybrid"
    PRUNING = "pruning"
    ABSTRACTION = "abstraction"


class TokenizerBackend(str, Enum):
    """Available tokenizer backends."""
    TIKTOKEN = "tiktoken"
    HUGGINGFACE = "huggingface"
    AUTO = "auto"


@dataclass
class CompressionConfig:
    """Configuration for prompt compression.

    Attributes:
        strategy: Compression strategy to use.
        target_ratio: Target compression ratio (0.0-1.0). 0.5 means 50% reduction.
        min_quality: Minimum quality score (0.0-1.0) for compressed output.
        max_iterations: Maximum compression iterations.
        preserve_patterns: Regex patterns or strings to preserve during compression.
        tokenizer_backend: Tokenizer backend to use.
        model_name: Model name for tokenizer (e.g., "gpt-4", "claude-3").
        verbose: Whether to print compression details.
        custom_strategies: Custom strategy configurations.
    """
    strategy: CompressionStrategy = CompressionStrategy.HYBRID
    target_ratio: float = 0.3
    min_quality: float = 0.70
    max_iterations: int = 3
    preserve_patterns: List[str] = field(default_factory=list)
    tokenizer_backend: TokenizerBackend = TokenizerBackend.AUTO
    model_name: Optional[str] = None
    verbose: bool = False
    custom_strategies: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration."""
        if not 0.0 < self.target_ratio <= 1.0:
            raise ValueError("target_ratio must be between 0.0 and 1.0")
        if not 0.0 <= self.min_quality <= 1.0:
            raise ValueError("min_quality must be between 0.0 and 1.0")
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
