#!/usr/bin/env python3
"""
Prompt Bonsai — Basic Usage Examples
====================================

Run: python basic_usage.py
"""

from prompt_bonsai import compress, Compressor


def example_1_one_shot():
    """Simplest possible usage."""
    print("=" * 60)
    print("Example 1: One-shot compression")
    print("=" * 60)

    long_prompt = """
    I would like to kindly request your assistance with a very important matter.
    Please, if you could, help me understand the fundamental principles of quantum
    mechanics. It would be great if you could provide a comprehensive explanation
    that covers wave-particle duality, the uncertainty principle, quantum
    entanglement, and superposition. I am wondering if you might be able to
    include specific examples and analogies to make these complex concepts more
    accessible and easier to understand. Thank you very much in advance for
    your help with this matter.
    """

    # Compress to 50% of original
    compressed = compress(long_prompt, ratio=0.5)

    print(f"Original length: {len(long_prompt)} chars")
    print(f"Compressed length: {len(compressed)} chars")
    print(f"\nCompressed prompt:\n{compressed}")


def example_2_with_compressor():
    """Using the Compressor class for more control."""
    print("\n" + "=" * 60)
    print("Example 2: Compressor class with verbose output")
    print("=" * 60)

    compressor = Compressor(
        strategy="hybrid",
        target_ratio=0.4,
        min_quality=0.85,
        verbose=True,
    )

    prompt = """
    System: You are an expert Python developer with 20 years of experience.
    Please review the following code and suggest improvements for readability,
    performance, and maintainability. Consider PEP 8 compliance, type hints,
    documentation, error handling, and testing coverage in your analysis.
    """

    result = compressor.compress(prompt)
    print(f"\nQuality score: {result.quality_report.overall_score:.3f}")


def example_3_preserve_patterns():
    """Preserving template variables."""
    print("\n" + "=" * 60)
    print("Example 3: Preserving template variables")
    print("=" * 60)

    template = """
    Please analyze the following user data and provide insights:

    User: {user_name}
    Age: {user_age}
    Location: {user_location}

    Please be thorough and provide specific recommendations tailored to this user.
    """

    # Preserve template variables
    compressed = compress(template, ratio=0.3, preserve=["{user_name}", "{user_age}"])

    print(f"Original:\n{template}")
    print(f"\nCompressed:\n{compressed}")
    print(f"\nVariables preserved: {all(v in compressed for v in ['{user_name}', '{user_age}'])}")


def example_4_different_strategies():
    """Comparing different strategies."""
    print("\n" + "=" * 60)
    print("Example 4: Comparing compression strategies")
    print("=" * 60)

    prompt = """
    Hello! I was wondering if you could please help me with something.
    I would like to understand how machine learning models work,
    specifically deep neural networks and transformer architectures.
    It would be really great if you could explain this in simple terms
    with some very specific examples. Thank you so much!
    """

    for strategy in ["semantic", "structural", "hybrid"]:
        compressor = Compressor(strategy=strategy, target_ratio=0.4)
        result = compressor.compress(prompt)

        savings = result.original_tokens - result.compressed_tokens
        print(f"\n{strategy.upper()}:")
        print(f"  Original tokens: {result.original_tokens}")
        print(f"  Compressed tokens: {result.compressed_tokens}")
        print(f"  Saved: {savings} ({savings/result.original_tokens*100:.1f}%)")
        print(f"  Quality: {result.quality_report.overall_score:.3f}")


def example_5_batch_compression():
    """Compress multiple prompts efficiently."""
    print("\n" + "=" * 60)
    print("Example 5: Batch compression with stats")
    print("=" * 60)

    prompts = [
        "Please explain " + "in great detail " * 10 + "how Python works",
        "I would like to kindly request " + "a very thorough " * 5 + "explanation of async/await",
        "Could you please " + "provide a comprehensive " * 8 + "guide to type hints?",
    ]

    compressor = Compressor(strategy="hybrid", target_ratio=0.5)

    for prompt in prompts:
        compressor.compress(prompt)

    stats = compressor.stats()
    print(f"Total compressions: {stats['total_compressions']}")
    print(f"Total tokens saved: {stats['total_tokens_saved']}")
    print(f"Average savings: {stats['avg_savings_percentage']:.1f}%")
    print(f"Estimated cost savings: ${stats['total_estimated_savings_usd']:.4f}")


if __name__ == "__main__":
    example_1_one_shot()
    example_2_with_compressor()
    example_3_preserve_patterns()
    example_4_different_strategies()
    example_5_batch_compression()
