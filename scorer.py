"""
judge() measures the generate stage: it checks whether the answer contains the
`expects` fact. judge_retrieval() measures the retrieve stage: it checks whether
any retrieved chunk contains that fact (criterion 1). Criteria 2, 4 and 5 are
read by hand off the run log.
"""

import re

import gate


# Stripping all whitespace lets "8 to 10" match "8 to 10 hours"; the tradeoff is it can match across word boundaries.
def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", "", text)


def judge(question: str, expects: str, answer: str, results) -> bool:
    if not expects or not expects.strip():
        return False
    if not results:
        return False
    if not answer or normalize(answer) == normalize(gate.REFUSAL):
        return False
    return normalize(expects) in normalize(answer)


def judge_retrieval(question: str, expects: str, results) -> bool:
    if not expects or not expects.strip():
        return False
    if not results:
        return False
    return any(normalize(expects) in normalize(result.text) for result in results)
