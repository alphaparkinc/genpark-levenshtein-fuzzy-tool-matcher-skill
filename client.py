"""Levenshtein Fuzzy Tool Matcher.
100% Python Standard Library.
"""
from typing import Dict, Any, List, Tuple

class LevenshteinFuzzyToolMatcher:
    """Fast Levenshtein distance and fuzzy similarity matcher for tool hallucination repair."""

    @staticmethod
    def compute_distance(s1: str, s2: str) -> Tuple[int, float]:
        if s1 == s2:
            return 0, 1.0
        len1, len2 = len(s1), len(s2)
        if len1 == 0:
            return len2, 0.0
        if len2 == 0:
            return len1, 0.0

        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                )
                if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)

        dist = dp[len1][len2]
        max_len = max(len1, len2)
        sim = 1.0 - (dist / max_len)
        return dist, round(sim, 4)

    @classmethod
    def find_best_match(cls, target: str, candidates: List[str], min_similarity: float = 0.6) -> Dict[str, Any]:
        best_candidate = None
        best_sim = -1.0
        best_dist = 9999

        for c in candidates:
            dist, sim = cls.compute_distance(target.lower(), c.lower())
            if sim > best_sim:
                best_sim = sim
                best_dist = dist
                best_candidate = c

        is_match = best_sim >= min_similarity
        return {
            "target": target,
            "matched_candidate": best_candidate if is_match else None,
            "similarity": best_sim if is_match else 0.0,
            "edit_distance": best_dist if is_match else -1,
            "is_confident": best_sim >= 0.8
        }

    @classmethod
    def suggest_alternatives(cls, target: str, candidates: List[str], top_k: int = 3) -> List[Dict[str, Any]]:
        scored = []
        for c in candidates:
            dist, sim = cls.compute_distance(target.lower(), c.lower())
            scored.append({"candidate": c, "distance": dist, "similarity": sim})
        scored.sort(key=lambda x: (-x["similarity"], x["distance"]))
        return scored[:top_k]
