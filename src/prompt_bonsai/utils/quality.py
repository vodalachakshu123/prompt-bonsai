"""Quality assessment utilities for prompt-bonsai."""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

import numpy as np


@dataclass
class QualityReport:
    """Quality assessment report for compressed prompt."""
    overall_score: float
    semantic_similarity: float
    structural_integrity: float
    information_retention: float
    readability_score: float
    preserved_keywords: List[str]
    warnings: List[str]
    details: Dict[str, Any]


class QualityAssessor:
    """Assess quality of compressed prompts."""

    def __init__(self) -> None:
        self._embedding_model = None

    def assess(
        self,
        original: str,
        compressed: str,
        preserve_patterns: Optional[List[str]] = None,
    ) -> QualityReport:
        """Assess quality of compressed prompt against original.

        Returns a QualityReport with scores from 0.0 to 1.0.
        """
        warnings = []

        # Semantic similarity (Jaccard + word overlap)
        semantic_sim = self._semantic_similarity(original, compressed)

        # Structural integrity (check for broken brackets, quotes, etc.)
        struct_integrity = self._structural_integrity(original, compressed)
        if struct_integrity < 0.9:
            warnings.append("Potential structural damage detected")

        # Information retention (keyword preservation)
        info_retention, preserved = self._information_retention(
            original, compressed, preserve_patterns
        )

        # Readability
        readability = self._readability_score(compressed)

        # Overall score (weighted average)
        overall = (
            semantic_sim * 0.35 +
            struct_integrity * 0.25 +
            info_retention * 0.25 +
            readability * 0.15
        )

        if overall < 0.7:
            warnings.append("Overall quality below acceptable threshold")

        return QualityReport(
            overall_score=overall,
            semantic_similarity=semantic_sim,
            structural_integrity=struct_integrity,
            information_retention=info_retention,
            readability_score=readability,
            preserved_keywords=preserved,
            warnings=warnings,
            details={
                "original_length": len(original),
                "compressed_length": len(compressed),
                "length_ratio": len(compressed) / max(len(original), 1),
            },
        )

    def _semantic_similarity(self, original: str, compressed: str) -> float:
        """Calculate semantic similarity using word overlap."""
        orig_words = set(self._normalize(original).split())
        comp_words = set(self._normalize(compressed).split())

        if not orig_words:
            return 1.0

        intersection = len(orig_words & comp_words)
        union = len(orig_words | comp_words)

        if union == 0:
            return 1.0

        return intersection / union

    def _structural_integrity(self, text: str, compressed: str) -> float:
        """Check structural integrity (balanced brackets, quotes, etc.)."""
        score = 1.0

        # Check balanced brackets
        for open_char, close_char in [("(", ")"), ("[", "]"), ("{", "}"), ("<", ">")]:
            orig_open = text.count(open_char)
            orig_close = text.count(close_char)
            comp_open = compressed.count(open_char)
            comp_close = compressed.count(close_char)

            if orig_open == orig_close and comp_open != comp_close:
                score -= 0.2

            if orig_open > 0 and comp_open == 0:
                score -= 0.1

        # Check balanced quotes
        orig_quotes = text.count(""") % 2 == 0
        comp_quotes = compressed.count(""") % 2 == 0
        if orig_quotes and not comp_quotes:
            score -= 0.15

        return max(0.0, score)

    def _information_retention(
        self,
        original: str,
        compressed: str,
        preserve_patterns: Optional[List[str]],
    ) -> tuple[float, List[str]]:
        """Check if important keywords/patterns are preserved."""
        preserved = []

        if preserve_patterns:
            for pattern in preserve_patterns:
                if pattern in compressed:
                    preserved.append(pattern)

        # Extract and check important keywords (capitalized words, technical terms)
        important_words = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', original)
        if important_words:
            retained = sum(1 for w in important_words if w.lower() in compressed.lower())
            ratio = retained / len(important_words)
        else:
            ratio = 1.0

        return ratio, preserved

    def _readability_score(self, text: str) -> float:
        """Simple readability assessment."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0.5

        words = text.split()
        avg_sentence_length = len(words) / max(len(sentences), 1)

        # Ideal: 15-20 words per sentence
        if avg_sentence_length <= 25:
            return 1.0
        elif avg_sentence_length <= 40:
            return 0.7
        else:
            return 0.4

    def _normalize(self, text: str) -> str:
        """Normalize text for comparison."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
