#!/usr/bin/env python3
"""
Prompt Bonsai — Benchmark Suite
================================

Run comprehensive benchmarks against standard datasets.

Usage:
    python run_benchmarks.py [--dataset DATASET] [--strategies STRATEGIES]
"""

import argparse
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict

from prompt_bonsai import Compressor


@dataclass
class BenchmarkResult:
    """Result for a single benchmark run."""
    strategy: str
    dataset: str
    num_prompts: int
    avg_original_tokens: float
    avg_compressed_tokens: float
    avg_savings_percent: float
    avg_quality_score: float
    avg_time_ms: float
    total_tokens_saved: int


def load_dataset(name: str) -> List[str]:
    """Load a benchmark dataset."""
    dataset_path = Path(__file__).parent / "datasets" / f"{name}.json"

    if dataset_path.exists():
        with open(dataset_path) as f:
            data = json.load(f)
            return data.get("prompts", [])

    # Fallback: generate synthetic dataset
    return generate_synthetic_dataset(name)


def generate_synthetic_dataset(name: str, size: int = 100) -> List[str]:
    """Generate a synthetic benchmark dataset."""
    templates = {
        "conversational": [
            "I would like to kindly request that you please help me understand {topic}. "
            "It would be really great if you could provide a very comprehensive explanation.",
            "Hello! I was wondering if you might be able to explain {topic} in quite simple terms. "
            "I am actually quite new to this subject.",
        ],
        "technical": [
            "Analyze the following JSON data and provide insights: {data}",
            "Review this Python code for bugs and performance issues: {code}",
        ],
        "mixed": [
            "Please help with {topic}. Here is the context: {context}",
        ],
    }

    import random

    prompts = []
    template_list = templates.get(name, templates["mixed"])

    topics = ["machine learning", "quantum computing", "blockchain", "kubernetes", "rust"]
    contexts = ["Some detailed context here... " * 20] * size

    for i in range(size):
        template = random.choice(template_list)
        prompt = template.format(
            topic=random.choice(topics),
            data='{"key": "value"}',
            code="def hello(): pass",
            context=contexts[i % len(contexts)],
        )
        prompts.append(prompt)

    return prompts


def run_benchmark(
    dataset: List[str],
    strategy: str,
    target_ratio: float = 0.4,
) -> BenchmarkResult:
    """Run benchmark for a strategy."""
    compressor = Compressor(strategy=strategy, target_ratio=target_ratio)

    total_original = 0
    total_compressed = 0
    total_quality = 0.0
    total_time = 0.0

    for prompt in dataset:
        start = time.perf_counter()
        result = compressor.compress(prompt)
        elapsed = (time.perf_counter() - start) * 1000

        total_original += result.original_tokens
        total_compressed += result.compressed_tokens
        total_quality += result.quality_report.overall_score
        total_time += elapsed

    n = len(dataset)

    return BenchmarkResult(
        strategy=strategy,
        dataset="synthetic",
        num_prompts=n,
        avg_original_tokens=total_original / n,
        avg_compressed_tokens=total_compressed / n,
        avg_savings_percent=(1 - total_compressed / total_original) * 100,
        avg_quality_score=total_quality / n,
        avg_time_ms=total_time / n,
        total_tokens_saved=total_original - total_compressed,
    )


def print_results(results: List[BenchmarkResult]) -> None:
    """Print benchmark results in a table."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Prompt Bonsai Benchmarks")

    table.add_column("Strategy", style="cyan")
    table.add_column("Prompts", justify="right")
    table.add_column("Orig Tokens", justify="right")
    table.add_column("Comp Tokens", justify="right")
    table.add_column("Savings %", justify="right", style="green")
    table.add_column("Quality", justify="right", style="yellow")
    table.add_column("Time (ms)", justify="right")

    for r in results:
        table.add_row(
            r.strategy,
            str(r.num_prompts),
            f"{r.avg_original_tokens:.1f}",
            f"{r.avg_compressed_tokens:.1f}",
            f"{r.avg_savings_percent:.1f}%",
            f"{r.avg_quality_score:.3f}",
            f"{r.avg_time_ms:.2f}",
        )

    console.print(table)

    # Summary
    total_saved = sum(r.total_tokens_saved for r in results)
    console.print(f"\n[bold green]Total tokens saved across all runs: {total_saved:,}[/]")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Prompt Bonsai benchmarks")
    parser.add_argument("--dataset", default="mixed", help="Dataset to use")
    parser.add_argument("--strategies", default="semantic,structural,hybrid",
                       help="Comma-separated list of strategies")
    parser.add_argument("--ratio", type=float, default=0.4,
                       help="Target compression ratio")
    args = parser.parse_args()

    strategies = [s.strip() for s in args.strategies.split(",")]
    dataset = load_dataset(args.dataset)

    print(f"Loaded {len(dataset)} prompts from dataset '{args.dataset}'")
    print(f"Testing strategies: {', '.join(strategies)}")
    print(f"Target ratio: {args.ratio}")
    print("-" * 60)

    results = []
    for strategy in strategies:
        print(f"Running {strategy}...")
        result = run_benchmark(dataset, strategy, args.ratio)
        results.append(result)

    print_results(results)

    # Save results
    output = Path("benchmark_results.json")
    with open(output, "w") as f:
        json.dump([asdict(r) for r in results], f, indent=2)
    print(f"\nResults saved to {output}")


if __name__ == "__main__":
    main()
