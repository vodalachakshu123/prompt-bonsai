#!/usr/bin/env python3
"""
Prompt Bonsai — Batch Processing
================================

Efficiently compress large batches of prompts with progress tracking.

Run: python batch_compression.py
"""

import concurrent.futures
from dataclasses import dataclass
from typing import List, Callable

from prompt_bonsai import Compressor, CompressionResult


@dataclass
class BatchResult:
    """Result of batch compression."""
    original_texts: List[str]
    compressed_texts: List[str]
    results: List[CompressionResult]
    total_tokens_saved: int
    avg_quality_score: float


def compress_batch(
    prompts: List[str],
    strategy: str = "hybrid",
    ratio: float = 0.4,
    max_workers: int = 4,
    progress_callback: Callable[[int, int], None] = None,
) -> BatchResult:
    """Compress a batch of prompts in parallel.

    Args:
        prompts: List of prompts to compress.
        strategy: Compression strategy.
        ratio: Target compression ratio.
        max_workers: Number of parallel workers.
        progress_callback: Called with (completed, total) for progress updates.

    Returns:
        BatchResult with all compression results.
    """
    compressor = Compressor(strategy=strategy, target_ratio=ratio)
    results = []

    def compress_one(prompt: str) -> CompressionResult:
        return compressor.compress(prompt)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(compress_one, p) for p in prompts]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            results.append(future.result())
            if progress_callback:
                progress_callback(i + 1, len(prompts))

    total_saved = sum(
        r.original_tokens - r.compressed_tokens for r in results
    )
    avg_quality = sum(r.quality_report.overall_score for r in results) / len(results)

    return BatchResult(
        original_texts=prompts,
        compressed_texts=[r.text for r in results],
        results=results,
        total_tokens_saved=total_saved,
        avg_quality_score=avg_quality,
    )


def example():
    """Example batch processing."""
    print("=" * 60)
    print("Batch Compression Example")
    print("=" * 60)

    prompts = [
        "I would like to kindly request a detailed explanation of " * 5 + topic
        for topic in [
            "Python metaclasses",
            "Rust ownership system",
            "Go concurrency patterns",
            "TypeScript advanced types",
            "Kubernetes networking",
            "GraphQL vs REST",
            "CQRS architecture",
            "Event sourcing patterns",
        ]
    ]

    def show_progress(completed: int, total: int):
        print(f"Progress: {completed}/{total}")

    result = compress_batch(
        prompts,
        strategy="hybrid",
        ratio=0.4,
        max_workers=4,
        progress_callback=show_progress,
    )

    print(f"\n{'='*60}")
    print("Results Summary")
    print(f"{'='*60}")
    print(f"Total prompts: {len(prompts)}")
    print(f"Total tokens saved: {result.total_tokens_saved}")
    print(f"Average quality score: {result.avg_quality_score:.3f}")
    print(f"Estimated savings: ${result.total_tokens_saved / 1000 * 0.01:.2f}")


if __name__ == "__main__":
    example()
