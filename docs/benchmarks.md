# Benchmarks

Run benchmarks to compare strategies:

```bash
python benchmarks/run_benchmarks.py --dataset mixed --strategies semantic,structural,hybrid
```

## Sample Results

| Strategy | Avg Savings | Avg Quality | Avg Time |
|----------|-------------|-------------|----------|
| Semantic | 35% | 0.92 | 12ms |
| Structural | 45% | 0.88 | 8ms |
| Hybrid | 42% | 0.91 | 15ms |

Results vary based on prompt content and length.
