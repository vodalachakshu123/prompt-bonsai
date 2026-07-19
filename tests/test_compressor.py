"""Tests for the main Compressor API."""

import pytest

from prompt_bonsai import Compressor, compress
from prompt_bonsai.config import CompressionConfig, CompressionStrategy
from prompt_bonsai.exceptions import StrategyError, QualityError


class TestCompressorInitialization:
    """Test compressor initialization."""

    def test_default_initialization(self):
        """Test compressor with default settings."""
        c = Compressor()
        assert c.config.strategy == CompressionStrategy.HYBRID
        assert c.config.target_ratio == 0.5

    def test_custom_initialization(self):
        """Test compressor with custom settings."""
        c = Compressor(
            strategy="semantic",
            target_ratio=0.3,
            min_quality=0.95,
            preserve=["{variable}"],
            model_name="gpt-4",
            verbose=False,
        )
        assert c.config.strategy == CompressionStrategy.SEMANTIC
        assert c.config.target_ratio == 0.3
        assert c.config.min_quality == 0.95
        assert "{variable}" in c.config.preserve_patterns

    def test_invalid_strategy(self):
        """Test compressor with invalid strategy."""
        with pytest.raises(StrategyError):
            Compressor(strategy="invalid")

    def test_config_override(self):
        """Test that config object overrides other params."""
        config = CompressionConfig(
            strategy=CompressionStrategy.STRUCTURAL,
            target_ratio=0.2,
        )
        c = Compressor(strategy="semantic", target_ratio=0.5, config=config)
        assert c.config.strategy == CompressionStrategy.STRUCTURAL
        assert c.config.target_ratio == 0.2


class TestCompressFunction:
    """Test the one-shot compress function."""

    def test_basic_compression(self, long_prompt):
        """Test basic one-shot compression."""
        result = compress(long_prompt, ratio=0.3, strategy="semantic")
        assert isinstance(result, str)
        assert len(result) < len(long_prompt)

    def test_compression_with_preserve(self):
        """Test preserving specific patterns."""
        prompt = "Please tell me about {user_name} and their {attribute}"
        result = compress(prompt, ratio=0.3, preserve=["{user_name}"])
        assert "{user_name}" in result

    def test_no_compression_needed(self):
        """Test very short prompt doesn't change much."""
        prompt = "Hello world"
        result = compress(prompt, ratio=0.1)
        assert isinstance(result, str)


class TestCompressorCompress:
    """Test Compressor.compress method."""

    def test_returns_compression_result(self, compressor, long_prompt):
        """Test that compress returns CompressionResult."""
        result = compressor.compress(long_prompt)
        assert hasattr(result, "text")
        assert hasattr(result, "original_tokens")
        assert hasattr(result, "compressed_tokens")
        assert hasattr(result, "quality_report")

    def test_achieves_target_ratio(self, compressor, long_prompt):
        """Test that compression achieves near-target ratio."""
        result = compressor.compress(long_prompt, target_ratio=0.3)
        achieved_ratio = 1 - (result.compressed_tokens / result.original_tokens)
        # Should be close to 0.3, but not necessarily exact
        assert 0.15 <= achieved_ratio <= 0.5

    def test_quality_above_threshold(self, compressor, long_prompt):
        """Test that quality is above minimum threshold."""
        result = compressor.compress(long_prompt)
        assert result.quality_report.overall_score >= 0.7

    def test_preserves_patterns(self, compressor):
        """Test that preserve patterns are kept."""
        prompt = "Please analyze {data} and return {format}"
        result = compressor.compress(prompt, preserve=["{data}", "{format}"])
        assert "{data}" in result.text
        assert "{format}" in result.text

    def test_stats_tracking(self, compressor, long_prompt):
        """Test that stats are tracked."""
        compressor.compress(long_prompt)
        compressor.compress(long_prompt)
        stats = compressor.stats()
        assert stats["total_compressions"] == 2

    def test_reset_stats(self, compressor, long_prompt):
        """Test resetting stats."""
        compressor.compress(long_prompt)
        compressor.reset_stats()
        assert compressor.stats() == {}

    def test_estimate_tokens(self, compressor, long_prompt):
        """Test token estimation."""
        estimate = compressor.estimate(long_prompt)
        assert isinstance(estimate, int)
        assert estimate > 0


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_string(self, compressor):
        """Test compressing empty string."""
        result = compressor.compress("")
        assert result.text == ""

    def test_whitespace_only(self, compressor):
        """Test compressing whitespace-only string."""
        result = compressor.compress("   \n\n\t  ")
        assert result.text.strip() == ""

    def test_very_long_prompt(self, compressor):
        """Test with extremely long prompt."""
        prompt = "word " * 10000
        result = compressor.compress(prompt, target_ratio=0.5)
        assert result.compressed_tokens < result.original_tokens

    def test_high_compression_ratio(self, long_prompt):
        """Test with very high compression ratio."""
        c = Compressor(target_ratio=0.8, min_quality=0.5)
        result = c.compress(long_prompt)
        assert result.compressed_tokens < result.original_tokens
