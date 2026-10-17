from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

from .filtering import clean_text
from .models import CandidateRule, ReviewComment

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_:\-\.]*")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
GENERIC_ANCHORS = {
    "package.json", "cargo.toml", "readme.md", "pyproject.toml", "tsconfig.json",
    "github", "main", "master", "src", "test", "tests",
}

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "because", "been", "but", "by",
    "can", "could", "do", "does", "for", "from", "had", "has", "have", "here", "i",
    "if", "in", "into", "is", "it", "just", "like", "maybe", "more", "not", "of", "on",
    "or", "our", "please", "so", "should", "that", "the", "then", "there", "these", "this",
    "to", "use", "using", "was", "we", "with", "would", "you", "your", "instead", "prefer",
}


def _stem(token: str) -> str:
    t = token.lower().strip("._-:")
    for suffix in ("ing", "edly", "ed", "es", "s"):
        if len(t) > 5 and t.endswith(suffix):
            t = t[: -len(suffix)]
            break
    return t


def tokenize(text: str) -> list[str]:
    out: list[str] = []
    for raw in TOKEN_RE.findall(clean_text(text)):
        t = _stem(raw)
        if len(t) < 3 or t in STOPWORDS:
            continue
        out.append(t)
    return out


def _normalized_anchor(raw: str) -> str | None:
    token = raw.strip("._-:")
    if len(token) < 5:
        return None
    normalized = token.lower()
    if normalized in GENERIC_ANCHORS:
        return None
    return normalized


def anchor_tokens(text: str) -> set[str]:
    """Return exact repo-specific identifiers that can bridge paraphrased feedback.

    Stable symbols such as ``camelCase``, ``nextTestSetup`` and
    ``ConfigBuilder::default`` are useful anchors even when surrounding prose is
    very different. Plain hyphenated English prose is intentionally *not* a
    strong anchor: the public Next.js pilot showed that a shared phrase such as
    ``follow-up`` can otherwise connect unrelated reviews.

    Hyphenated identifiers are still accepted when reviewers mark them as code
    with Markdown backticks.
    """
    cleaned = clean_text(text)
    anchors: set[str] = set()

    # Backticks are an explicit signal that a token is code/project vocabulary,
    # so they may safely preserve kebab-case identifiers.
    for span in BACKTICK_RE.findall(cleaned):
        for raw in TOKEN_RE.findall(span):
            normalized = _normalized_anchor(raw)
            if normalized is None:
                continue
            looks_code_like = (
                raw.startswith("_")
                or "_" in raw
                or "." in raw
                or "::" in raw
                or "-" in raw
                or re.search(r"[a-z][A-Z]", raw) is not None
            )
            if looks_code_like:
                anchors.add(normalized)

    # Outside code spans, require a stronger structural signal than a single
    # hyphen so natural prose like "follow-up" does not become repository policy.
    for raw in TOKEN_RE.findall(cleaned):
        normalized = _normalized_anchor(raw)
        if normalized is None:
            continue
        looks_structured = (
            raw.startswith("_")
            or "_" in raw
            or "." in raw
            or "::" in raw
            or re.search(r"[a-z][A-Z]", raw) is not None
        )
        if looks_structured:
            anchors.add(normalized)
    return anchors


def _idf_vectors(token_lists: list[list[str]]) -> list[dict[str, float]]:
    n = max(1, len(token_lists))
    df: Counter[str] = Counter()
    for toks in token_lists:
        df.update(set(toks))
    vectors: list[dict[str, float]] = []
    for toks in token_lists:
        tf = Counter(toks)
        vec: dict[str, float] = {}
        for token, count in tf.items():
            idf = math.log((1 + n) / (1 + df[token])) + 1.0
            vec[token] = (1.0 + math.log(count)) * idf
        vectors.append(vec)
    return vectors


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def cluster_comments(
    comments: list[ReviewComment],
    *,
    similarity_threshold: float = 0.34,
    min_unique_prs: int = 2,
) -> list[CandidateRule]:
    if not comments:
        return []
    token_lists = [tokenize(c.body) for c in comments]
    anchors = [anchor_tokens(c.body) for c in comments]
    vectors = _idf_vectors(token_lists)
    uf = _UnionFind(len(comments))

    for i in range(len(comments)):
        set_i = set(token_lists[i])
        for j in range(i + 1, len(comments)):
            if comments[i].pr_number == comments[j].pr_number:
                continue
            shared = set_i & set(token_lists[j])
            shared_anchors = anchors[i] & anchors[j]
            if len(shared) < 2 and not shared_anchors:
                continue
            sim = cosine(vectors[i], vectors[j])
            # Exact repo-specific identifiers can connect paraphrased review feedback.
            # Keep a small lexical floor so one incidental symbol mention is not enough.
            identifier_bonus = any(("_" in t or "." in t or ":" in t) for t in shared)
            threshold = similarity_threshold - (0.05 if identifier_bonus else 0.0)
            if shared_anchors:
                threshold = min(threshold, 0.03)
            if sim >= threshold:
                uf.union(i, j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(comments)):
        groups[uf.find(i)].append(i)

    candidates: list[CandidateRule] = []
    for idxs in groups.values():
        prs = {comments[i].pr_number for i in idxs}
        if len(prs) < min_unique_prs:
            continue

        # Pick the medoid: the evidence comment most similar to the rest.
        best_i = idxs[0]
        best_score = -1.0
        for i in idxs:
            sims = [cosine(vectors[i], vectors[j]) for j in idxs if i != j]
            score = sum(sims) / max(1, len(sims))
            if score > best_score:
                best_i, best_score = i, score

        common = Counter()
        for i in idxs:
            common.update(set(token_lists[i]))
        common_tokens = [t for t, count in common.most_common(12) if count >= 2]
        evidence = sorted((comments[i] for i in idxs), key=lambda c: (c.pr_number, c.url))
        candidates.append(
            CandidateRule(
                rule_id="",
                representative=clean_text(comments[best_i].body),
                comments=evidence,
                score=best_score,
                tokens=common_tokens,
            )
        )

    candidates.sort(key=lambda c: (c.unique_prs, c.unique_reviewers, c.score), reverse=True)
    for n, candidate in enumerate(candidates, 1):
        candidate.rule_id = f"MB-{n:03d}"
    return candidates
