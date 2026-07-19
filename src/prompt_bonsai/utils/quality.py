"""Quality assessment utilities for prompt-bonsai."""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


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
        pass

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

        # Semantic similarity - weighted by word importance
        semantic_sim = self._semantic_similarity(original, compressed)

        # Structural integrity
        struct_integrity = self._structural_integrity(original, compressed)
        if struct_integrity < 0.8:
            warnings.append("Potential structural damage detected")

        # Information retention
        info_retention, preserved = self._information_retention(
            original, compressed, preserve_patterns
        )

        # Readability
        readability = self._readability_score(compressed)

        # Overall score - weighted average with forgiveness for good compression
        # If semantic similarity is decent and structure is intact, boost score
        overall = (
            semantic_sim * 0.30 +
            struct_integrity * 0.25 +
            info_retention * 0.25 +
            readability * 0.20
        )

        # Forgiveness: if we removed mostly filler words (good compression),
        # don't penalize too hard
        if semantic_sim > 0.5 and struct_integrity > 0.9 and info_retention > 0.8:
            overall = min(1.0, overall + 0.1)

        if overall < 0.5:
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
        """Calculate semantic similarity using weighted word overlap.

        Gives higher weight to content words (nouns, verbs) vs filler words.
        """
        # Define filler words that are okay to lose
        filler_words = {
            'please', 'kindly', 'would', 'could', 'should', 'may', 'might',
            'very', 'really', 'quite', 'rather', 'pretty', 'fairly',
            'just', 'actually', 'basically', 'honestly', 'literally',
            'essentially', 'simply', 'obviously', 'definitely', 'certainly',
            'probably', 'maybe', 'perhaps', 'possibly', 'likely',
            'thank', 'thanks', 'appreciate', 'grateful',
            'want', 'like', 'need', 'help', 'assist',
            'great', 'good', 'nice', 'wonderful', 'excellent',
        }

        orig_words = self._normalize(original).split()
        comp_words = self._normalize(compressed).split()

        if not orig_words:
            return 1.0

        # Build word sets with weights
        orig_content = set()
        orig_filler = set()

        for w in orig_words:
            if w in filler_words or len(w) <= 2:
                orig_filler.add(w)
            else:
                orig_content.add(w)

        comp_set = set(comp_words)

        # Content words are worth 3x more than filler words
        content_match = len(orig_content & comp_set)
        filler_match = len(orig_filler & comp_set)

        total_weight = len(orig_content) * 3 + len(orig_filler)
        if total_weight == 0:
            return 1.0

        matched_weight = content_match * 3 + filler_match
        similarity = matched_weight / total_weight

        # If we lost a lot of content words, that's bad
        # If we lost mostly filler words, that's fine
        return min(1.0, similarity)

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
                score -= 0.15

            if orig_open > 0 and comp_open == 0:
                score -= 0.05

        # Check balanced double quotes
        orig_double = text.count('"') % 2 == 0
        comp_double = compressed.count('"') % 2 == 0
        if orig_double and not comp_double:
            score -= 0.1

        # Check balanced single quotes (only if they were balanced in original)
        orig_single = text.count("'") % 2 == 0
        comp_single = compressed.count("'") % 2 == 0
        if orig_single and not comp_single:
            score -= 0.1

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

        # Extract important keywords (capitalized words, technical terms, long words)
        important_words = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', original)
        # Also include words longer than 6 chars (likely content words)
        long_words = [w for w in original.split() if len(w) > 6]
        important_words.extend(long_words)

        if important_words:
            retained = sum(1 for w in important_words if w.lower() in compressed.lower())
            ratio = retained / len(important_words)
        else:
            ratio = 1.0

        return ratio, preserved

    def _readability_score(self, text: str) -> float:
        """Simple readability assessment."""
        if not text.strip():
            return 0.5

        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0.5

        words = text.split()
        avg_sentence_length = len(words) / max(len(sentences), 1)

        # Ideal: 15-25 words per sentence
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
