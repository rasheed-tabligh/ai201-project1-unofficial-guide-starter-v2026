# """
# Deciding whether an answer was right.

# `run_eval.py` imports this module and looks for exactly one function,
# `judge(question, expects, answer, results) -> bool`. The name and the shape of
# the signature are the handshake — get either wrong and the eval runs unscored
# and the Run columns come out blank.

# What "right" means here: the answer is not a refusal, and it contains the
# `expects` phrase written in `questions.py` before any results existed. Every
# `expects` in this corpus is a specific fact — $30, 7:00pm, 8 to 10, week two,
# $2.00 — so this is a substring check, not a judgment about phrasing.

# The comparison ignores case, spacing and the markdown the model likes to wrap
# numbers in, because "**7:00 pm**" and "7:00pm" are the same fact. It does NOT
# treat "2" and "two" as the same, or accept a near miss: if the model says
# "week 2" when I wrote "week two", that is a fail, and it should show up as one
# so I can decide whether the answer or the `expects` was the thing that was
# wrong.

# Criteria 2 and 5 — every answer names a source, and no claim comes from
# outside the retrieved chunks — are not decided here. Those are read off the
# run log by hand, because a source line being *present* is not the same as it
# being *correct*.
# """

# import re

# import gate
# from store import Result


# def normalize(text: str) -> str:
#     """
#     Flatten a string to the form the comparison happens in.

#     Lowercases, drops the markdown the model wraps facts in, and removes
#     whitespace entirely so "8 to 10" matches "8to10hours" from an answer that
#     said "8 to 10 hours a week".
#     """
#     text = text.lower()
#     text = re.sub(r"[*_`]", "", text)      # **7:00pm** and `$30` are the fact
#     return re.sub(r"\s+", "", text)


# def is_refusal(answer: str) -> bool:
#     """True when the gate or the model declined to answer."""
#     return normalize(answer) == normalize(gate.REFUSAL)


# def judge(question: str, expects: str, answer: str, results: list[Result]) -> bool:
#     """
#     Did this run answer the question correctly?

#     `question` is the question asked, `expects` the phrase from `questions.py`
#     that a correct answer has to contain, `answer` what the system produced,
#     and `results` the chunks retrieval handed the model.

#     Returns False for a refusal, for an empty retrieval, and for an answer that
#     doesn't contain `expects`. A question with no `expects` can't be judged at
#     all, so it doesn't count as a pass.
#     """
#     if not expects.strip():
#         return False

#     if not results:
#         return False

#     if not answer.strip() or is_refusal(answer):
#         return False

#     return normalize(expects) in normalize(answer)

def judge(question: str, expects: str, answer: str, results) -> bool:
    if not expects:
        return False
    return expects.strip().lower() in (answer or "").lower()