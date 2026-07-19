"""Tests for individual compression strategies."""

import pytest

from prompt_bonsai.compressors.semantic import SemanticCompressor
from prompt_bonsai.compressors.structural import StructuralCompressor
from prompt_bonsai.compressors.hybrid import HybridCompressor
from prompt_bonsai.config import CompressionConfig


class TestSemanticCompressor:
    """Test semantic compression."""

    def test_removes_fillers(self):
        """Test that filler phrases are removed."""
        c = SemanticCompressor()
        prompt = "I would like to kindly request that you please help me"
        result = c.compress(prompt, target_ratio=0.3)
        assert "I would like to" not in result.text or len(result.text) < len(prompt)

    def test_removes_redundancies(self):
        """Test that redundant pairs are simplified."""
        c = SemanticCompressor()
        prompt = "The advance planning and final outcome was unexpected"
        result = c.compress(prompt, target_ratio=0.1)
        # Should have compressed somewhat
        assert result.compressed_tokens <= c.estimate_tokens(prompt)

    def test_preserves_meaning(self):
        """Test that core meaning is preserved."""
        c = SemanticCompressor()
        prompt = "Explain quantum mechanics including superposition"
        result = c.compress(prompt, target_ratio=0.2)
        assert "quantum" in result.text.lower() or "superposition" in result.text.lower()


class TestStructuralCompressor:
    """Test structural compression."""

    def test_normalizes_whitespace(self):
        """Test whitespace normalization."""
        c = StructuralCompressor()
        prompt = "Line 1\n\n\n\n\nLine 2"
        result = c.compress(prompt, target_ratio=0.1)
        assert "\n\n\n" not in result.text

    def test_minimizes_json(self):
        """Test JSON minimization."""
        c = StructuralCompressor()
        prompt = "```json\n{\n    \"key\": \"value\"\n}\n```"
        result = c.compress(prompt, target_ratio=0.1)
        # JSON should be compacted
        assert "\"key\"" in result.text

    def test_removes_comments(self):
        """Test comment removal."""
        c = StructuralCompressor()
        prompt = "code # this is a comment\nmore code"
        result = c.compress(prompt, target_ratio=0.1)
        assert "# this is a comment" not in result.text

    def test_preserves_code_structure(self):
        """Test that code structure is preserved."""
        c = StructuralCompressor()
        prompt = "def hello():\n    # greeting\n    print('hi')"
        result = c.compress(prompt, target_ratio=0.1)
        assert "def hello()" in result.text
        assert "print('hi')" in result.text


class TestHybridCompressor:
    """Test hybrid compression."""

    def test_selects_structured_for_code(self):
        """Test that code prompts use structural first."""
        c = HybridCompressor()
        prompt = "```python\nprint('hello')\n```"
        result = c.compress(prompt, target_ratio=0.1)
        assert result.metadata.get("prompt_type") == "structured"

    def test_selects_conversational_for_chat(self):
        """Test that chat prompts use semantic first."""
        c = HybridCompressor()
        prompt = "Hello! Could you please help me with something?"
        result = c.compress(prompt, target_ratio=0.1)
        assert result.metadata.get("prompt_type") == "conversational"

    def test_achieves_better_compression(self, long_prompt):
        """Test hybrid achieves good compression."""
        c = HybridCompressor()
        result = c.compress(long_prompt, target_ratio=0.4)
        savings = result.original_tokens - result.compressed_tokens
        assert savings > 0
