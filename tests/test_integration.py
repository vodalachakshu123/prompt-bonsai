"""Integration tests for prompt-bonsai with external tools."""

import pytest


class TestLiteLLMIntegration:
    """Test integration with LiteLLM."""

    def test_compress_before_litellm(self):
        """Test compressing prompt before sending to LiteLLM."""
        pytest.importorskip("litellm", reason="litellm not installed")

        from prompt_bonsai import compress

        prompt = "Please explain the following in great detail: " * 20 + "quantum computing"
        compressed = compress(prompt, ratio=0.4)

        # Verify compressed prompt is usable
        assert len(compressed) > 0
        assert "quantum" in compressed.lower()


class TestOpenAIIntegration:
    """Test integration with OpenAI."""

    def test_compress_for_openai(self):
        """Test preparing prompt for OpenAI API."""
        from prompt_bonsai import Compressor

        compressor = Compressor(model_name="gpt-4", target_ratio=0.3)

        system_prompt = """You are a helpful assistant. Please provide detailed,
        accurate, and well-researched responses to all user queries. Always be
        polite, professional, and thorough in your explanations."""

        result = compressor.compress(system_prompt)

        # Should still be usable as system prompt
        assert len(result.text) > 0
        assert result.quality_report.overall_score > 0.7


class TestLangChainIntegration:
    """Test integration with LangChain."""

    def test_compress_langchain_prompt(self):
        """Test compressing a LangChain-style prompt."""
        from prompt_bonsai import compress

        template = """You are an expert in {field}. Please analyze the following:

        Context: {context}

        Question: {question}

        Please provide a detailed response with examples."""

        # Compress with variable preservation
        filled = template.format(
            field="machine learning",
            context="Neural networks are computational models... " * 50,
            question="How do transformers work?"
        )

        compressed = compress(filled, ratio=0.4, preserve=["{field}", "{question}"])

        assert "{field}" in compressed or "machine learning" in compressed
        assert len(compressed) < len(filled)
