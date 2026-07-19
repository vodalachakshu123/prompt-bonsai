"""Semantic compression strategy.

Removes redundant words, filler phrases, and low-information content
while preserving core meaning.
"""

import re
from typing import Optional, List

from prompt_bonsai.compressors.base import BaseCompressor
from prompt_bonsai.config import CompressionConfig


class SemanticCompressor(BaseCompressor):
    """Compress prompts by removing semantically redundant content."""

    # Filler phrases that can be removed without losing meaning
    FILLER_PATTERNS = [
        r'please',
        r'kindly',
        r'I would like to',
        r'I want to',
        r'I need you to',
        r'could you',
        r'would you',
        r'can you',
        r'it would be great if',
        r'it would be helpful if',
        r'if possible',
        r'if you could',
        r'I was wondering',
        r'I am wondering',
        r'just',
        r'really',
        r'very',
        r'quite',
        r'actually',
        r'basically',
        r'honestly',
        r'literally',
        r'essentially',
        r'in order to',
        r'due to the fact that',
        r'in spite of the fact that',
        r'at this point in time',
        r'in the event that',
        r'for the purpose of',
        r'with regard to',
        r'in reference to',
        r'in the process of',
        r'with the exception of',
        r'in the near future',
        r'at the present time',
        r'during the course of',
        r'in the final analysis',
        r'in the nature of',
        r'for all intents and purposes',
    ]

    # Redundant modifiers
    REDUNDANT_PAIRS = [
        (r'advance\s+planning', 'planning'),
        (r'end\s+result', 'result'),
        (r'final\s+outcome', 'outcome'),
        (r'free\s+gift', 'gift'),
        (r'past\s+history', 'history'),
        (r'true\s+facts', 'facts'),
        (r'unexpected\s+surprise', 'surprise'),
        (r'new\s+innovation', 'innovation'),
        (r'close\s+proximity', 'proximity'),
        (r'complete\s+absence', 'absence'),
        (r'exact\s+same', 'same'),
        (r'first\s+beginning', 'beginning'),
        (r'full\s+complement', 'complement'),
        (r'joint\s+collaboration', 'collaboration'),
        (r'mutual\s+cooperation', 'cooperation'),
        (r'positive\s+accomplishment', 'accomplishment'),
        (r'regular\s+routine', 'routine'),
        (r'revert\s+back', 'revert'),
        (r'serious\s+danger', 'danger'),
        (r'total\s+annihilation', 'annihilation'),
    ]

    def __init__(self, config: Optional[CompressionConfig] = None) -> None:
        super().__init__(config)
        self._last_iterations = 1

    def _compress_impl(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]] = None,
    ) -> str:
        """Compress by removing semantic redundancies."""
        compressed = text
        iteration = 0
        max_iter = self.config.max_iterations

        while (
            self.tokenizer.count(compressed) > target_tokens
            and iteration < max_iter
        ):
            iteration += 1

            # Phase 1: Remove filler phrases
            compressed = self._remove_fillers(compressed, preserve_patterns)

            # Phase 2: Remove redundant word pairs
            compressed = self._remove_redundancies(compressed)

            # Phase 3: Simplify verbose constructions
            compressed = self._simplify_constructions(compressed)

            # Phase 4: Remove redundant adverbs
            if iteration >= 2:
                compressed = self._remove_weak_adverbs(compressed)

            if self.tokenizer.count(compressed) <= target_tokens:
                break

        self._last_iterations = iteration
        return compressed.strip()

    def _remove_fillers(self, text: str, preserve_patterns: Optional[List[str]]) -> str:
        """Remove filler phrases."""
        result = text
        for pattern in self.FILLER_PATTERNS:
            # Check if pattern is in preserve list
            if preserve_patterns:
                clean_pattern = pattern.replace(r'', '').replace(r'\s+', ' ')
                if any(clean_pattern in p for p in preserve_patterns):
                    continue
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result)
        return result

    def _remove_redundancies(self, text: str) -> str:
        """Remove redundant word pairs."""
        result = text
        for pattern, replacement in self.REDUNDANT_PAIRS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

    def _simplify_constructions(self, text: str) -> str:
        """Simplify verbose grammatical constructions."""
        simplifications = [
            (r'in order to', 'to'),
            (r'due to the fact that', 'because'),
            (r'in spite of the fact that', 'although'),
            (r'in the event that', 'if'),
            (r'for the purpose of', 'for'),
            (r'with regard to', 'about'),
            (r'in reference to', 'about'),
            (r'with the exception of', 'except'),
            (r'despite the fact that', 'although'),
            (r'regardless of the fact that', 'although'),
            (r'for the reason that', 'because'),
            (r'on the grounds that', 'because'),
            (r'with respect to', 'about'),
            (r'in connection with', 'about'),
            (r'in relation to', 'about'),
            (r'pertaining to', 'about'),
            (r'reference to', 'about'),
        ]

        result = text
        for pattern, replacement in simplifications:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

    def _remove_weak_adverbs(self, text: str) -> str:
        """Remove weak adverbs that don't add meaning."""
        weak_adverbs = [
            r'very',
            r'really',
            r'quite',
            r'pretty',
            r'rather',
            r'fairly',
            r'extremely',
            r'incredibly',
            r'absolutely',
            r'completely',
            r'totally',
            r'utterly',
            r'highly',
            r'deeply',
            r'strongly',
        ]

        result = text
        for pattern in weak_adverbs:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        result = re.sub(r'\s+', ' ', result)
        return result
