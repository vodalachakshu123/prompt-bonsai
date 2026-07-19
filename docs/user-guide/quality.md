# Quality Assessment

Prompt Bonsai evaluates compressed prompts on four dimensions:

## Quality Metrics

### Semantic Similarity (35% weight)
Measures word overlap between original and compressed text using Jaccard similarity.

### Structural Integrity (25% weight)
Checks for broken brackets, quotes, and formatting.
- Balanced parentheses `()`, `[]`, `{}`, `<>`
- Balanced quotes `"`
- Preserved code structure

### Information Retention (25% weight)
- Preserves capitalized terms and technical keywords
- Tracks `preserve_patterns` retention
- Measures keyword coverage

### Readability Score (15% weight)
- Ideal sentence length: 15-25 words
- Penalizes overly long sentences
- Rewards clear structure

## QualityReport

```python
from prompt_bonsai import Compressor

compressor = Compressor(min_quality=0.90)
result = compressor.compress(prompt)

report = result.quality_report
print(f"Overall: {report.overall_score:.2f}")
print(f"Semantic: {report.semantic_similarity:.2f}")
print(f"Structural: {report.structural_integrity:.2f}")
print(f"Information: {report.information_retention:.2f}")
print(f"Readability: {report.readability_score:.2f}")

if report.warnings:
    print("Warnings:", report.warnings)
```

## Handling Low Quality

If compression falls below `min_quality`, a `QualityError` is raised:

```python
from prompt_bonsai import Compressor
from prompt_bonsai.exceptions import QualityError

compressor = Compressor(min_quality=0.95)

try:
    result = compressor.compress(prompt, target_ratio=0.8)
except QualityError as e:
    print(f"Compression too aggressive: {e}")
    # Fall back to gentler compression
    result = compressor.compress(prompt, target_ratio=0.4)
```
