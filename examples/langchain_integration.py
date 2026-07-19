#!/usr/bin/env python3
"""
Prompt Bonsai — LangChain Integration
=====================================

Shows how to integrate prompt-bonsai with LangChain for automatic
prompt compression before LLM calls.

Run: python langchain_integration.py
"""

from typing import Optional

from prompt_bonsai import Compressor


class CompressedPromptTemplate:
    """LangChain-compatible prompt template with automatic compression."""

    def __init__(
        self,
        template: str,
        compressor: Optional[Compressor] = None,
        compress_ratio: float = 0.3,
    ):
        self.template = template
        self.compressor = compressor or Compressor(target_ratio=compress_ratio)

    def format(self, **kwargs) -> str:
        """Format and compress the prompt."""
        # Format the template
        formatted = self.template.format(**kwargs)

        # Compress the result
        result = self.compressor.compress(formatted)

        return result.text


# Example usage with LangChain-style patterns
def example():
    """Example LangChain integration."""
    print("=" * 60)
    print("LangChain Integration Example")
    print("=" * 60)

    # Create a compressed prompt template
    template = CompressedPromptTemplate(
        template="""
        You are an expert in {domain}. Please provide a comprehensive analysis
        of the following situation. I would greatly appreciate it if you could
        be very thorough and detailed in your response, covering all possible
        angles and providing specific examples where appropriate.

        Context: {context}

        Please structure your response with clear headings and bullet points.
        """,
        compress_ratio=0.4,
    )

    # Use it like a normal template
    compressed_prompt = template.format(
        domain="cybersecurity",
        context="A company has detected unusual network traffic patterns "
                "suggesting a potential APT campaign. The traffic shows "
                "beaconing behavior to known C2 domains with encrypted payloads.",
    )

    print(f"\nCompressed prompt:\n{compressed_prompt}")
    print(f"\nLength: {len(compressed_prompt)} chars")


if __name__ == "__main__":
    example()
