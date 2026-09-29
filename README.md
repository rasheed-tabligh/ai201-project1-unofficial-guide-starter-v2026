# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The corpus is campus_life, 88 short posts written by students about dorms,
dining halls, courses and the administrative rules nobody explains properly.
The system answers specific factual questions about them — laundry prices,
course workloads, dining hall hours, add/drop deadlines — by retrieving the
chunks closest in meaning to the question and answering from those alone,
naming the source file each fact came from. A relevance gate checks the
distance of the best chunk before the model runs, so a question the documents
do not cover is refused rather than guessed at.

## Chunking Strategy

**Chunk size:** 400 characters (the ceiling used when merging paragraphs)
**Overlap:** none — chunks break on paragraph boundaries, so neighbouring
chunks share no text

The starter's fixed 800-character window never split anything in this corpus.
campus_life is 88 documents averaging 317 characters, so indexing produced 88
chunks from 88 documents — one whole post per chunk. That is not always the
right call. A file like housing_innisfree_hall.txt holds a building
description, a laundry line and a noise line in one post, and a question about
noise pulled all of it back with most of the text irrelevant.

So the strategy changed from cutting by length to cutting on structure.
split_documents splits each document on blank lines, then merges consecutive
paragraphs while the combined text stays under 400 characters, and folds
anything still under 100 characters into the chunk before it so single-line
paragraphs do not become fragments. The 400 ceiling comes from the corpus
itself — the longest document is 549 characters and the average is 317, so a
larger ceiling would merge posts back into one chunk and defeat the split.

The result is 99 chunks from 88 documents, averaging 281 characters, shortest
101 and longest 419. The shortest chunk rose from 178 to 101 only because
multi-topic posts now come apart, and no chunk is a fragment.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for BIOL 160 Cell Biology

People keep asking so: 9 to 11 hours a week, the heaviest first-year course by reputation. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_the_atrium.txt#0` — produced by: `chunker.py::split_documents`

```
The Atrium

Transferred in last year, so take this with a grain of salt. Wait times: no queue, it's all grab-and-go refrigerated cases. The thing worth going for is genuinely good sandwiches restocked twice a day. The thing to know is that picked clean by 1:15 and not restocked again until the next morning.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** What time does Halden Hall close?

**Answer:**

```
  (best distance 0.323, cutoff 0.55)

Halden Hall closes at 7:00pm. 

Sources: `dining_halden_hall.txt` and `dining_halden_hall_followup.txt`

Sources retrieved: dining_halden_hall.txt, dining_halden_hall_followup.txt, dining_north_kitchen_followup.txt, dining_pellew_dining_hall.txt, dining_pellew_dining_hall_followup.txt
```

**My relevance cutoff:**

0.55, measured rather than inherited. I ran my five in-corpus questions and the
five OUT_OF_SCOPE questions through `app.py retrieve` and recorded the best
distance for each. The two groups did not overlap anywhere: every in-corpus
question landed between 0.149 and 0.323, and every out-of-corpus question
landed between 0.825 and 0.934. That is a gap of half a distance unit with
nothing in it, so the cutoff had a wide window to sit in. I put it at 0.55,
near the middle of the gap, which leaves more room above my worst real question
(0.323) than below my closest out-of-corpus one (0.825). The starter's 0.6 also
falls in the gap and would have worked, but 0.55 is the number my own
measurements support.

One thing I got wrong in advance: I expected the Fenwick Court laundry question
to be the hard one, because the corpus has near-identical laundry posts for
seven different buildings and they differ only in the prices. It scored the
best of all five at 0.149, and the correct file came back first. The embedding
separated the buildings more cleanly than I expected.

| Question | In corpus? | Best distance |
|---|---|---|
| When does dropping a course start showing as a W on my transcript? | Yes | 0.213 |
| How much printing money does each student get per semester? | Yes | 0.319 |
| How many hours a week outside class does CS 210 take? | Yes | 0.300 |
| What time does Halden Hall close? | Yes | 0.323 |
| How much does a wash cost in Fenwick Court laundry? | Yes | 0.149 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.891 |

## How I Used AI

**1.** I asked Claude for help drafting my five test questions. It couldn't
write anything useful at first because it had no view of my documents, so I ran
`python app.py chunks -n 8` and gave it eight real chunks to work from. It
drafted five questions with `expects` phrases, all tied to specific facts —
a price, a time, a number, a rule. The thing I had to catch myself was whether
to swap in my own college's buildings instead. The answer was no: Halden Hall
and Fenwick Court only exist inside campus_life, so real buildings would have
left the system with nothing to retrieve and every question would have failed.

**2.** I decided the chunking strategy myself — split on blank lines, merge
short paragraphs — after seeing that the starter's 800-character window never
split anything in a corpus averaging 317 characters per document. I had Claude
Code implement it. It came back working, and it also flagged something I hadn't
asked about: the 100-character floor merges a short chunk into the previous
one, but a document whose *first* paragraph is under 100 characters has no
previous chunk, so it gets emitted short anyway. That doesn't happen on
campus_life — my shortest chunk is 101 — but it would on a corpus that opens
with short headers. I left it, knowing the limitation.

**3.** I had Claude Code review `scorer.py`. It raised four problems: an answer
of "7:00 PM" would fail against my `expects` of "7:00pm" because of the space; an
empty retrieval would still pass if the answer happened to contain the fact; a
refusal was never checked for explicitly; and `judge_retrieval` didn't compare
text the same way `judge` did. Two of those can't happen through the actual
pipeline. `gate.check` refuses when there are no results, so the model never
answers from an empty retrieval, and the refusal sentence doesn't contain any of
my `expects` phrases. The one that mattered wasn't on its list of false passes at
all. It was the inconsistency between the two functions: neither normalized whitespace, so the same fact spaced differently in a chunk and in an answer would have read as absent from the chunks but present in the answer. I put both on
the same `normalize()`, which strips case, markdown and whitespace. The cost is
that a match can now run across word boundaries.

**4.** After implementing BM25 hybrid retrieval I pasted the before and after
retrieval rankings for two questions into Claude and asked whether the change
had helped. It had not, and I would probably have recorded it as a success
from the run log alone, because all five criteria came out MET both times.
What the comparison showed was that my second Fenwick document had moved down
from rank 3 to rank 4 and that admin_printing_quota.txt had entered the top 5
at distance 0.7491, neither of which any of my criteria could see. That is
also where the gate risk came from: the Mongolia question's best distance
moving from 0.825 to 0.852 because hybrid pushed the closest chunk out of the
returned five. Honestly stated, I used Claude Code to write most of the code
changes in this unit and to draft these README sections from facts and
verdicts I supplied. The five criteria and all five verdicts are my own.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Source: `results/run_2026-09-28_2232_before.md`, produced by
`run_eval.py::main`. Corpus campus_life, top-k 5, cutoff 0.55, 3 runs per
question, caching off.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks stand on their own | 7 of 8 | 7/8 | n/a | n/a | MET |
| 5. Answers stay inside the retrieved chunks | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criteria 1 and 3 are measured once, not three times, because retrieval is
deterministic and the gate is a comparison against a fixed number; the same
value goes in all three columns. Criterion 4 is a one-off sample of 8 chunks,
not a per-run measurement, which is why runs 2 and 3 are n/a. Criterion 1
comes from `scorer.py::judge_retrieval`, which checks the retrieved chunks.
Criteria 2 and 5 were read by hand off the 15 answers in the log. For
criterion 5, all 15 answers were checked for prices, times and numbers not
present in the chunks they were given, and none were found.

**Real output, verbatim from the before log.** The five-question table:

| Question | Run 1 | Run 2 | Run 3 | Chunk had it |
|---|---|---|---|---|
| When does dropping a course start showing as a W on my transcript? | pass | pass | pass | yes |
| How much printing money does each student get per semester? | pass | pass | pass | yes |
| How many hours a week outside class does CS 210 take? | pass | pass | pass | yes |
| What time does Halden Hall close? | pass | pass | pass | yes |
| How much does a wash cost in Fenwick Court laundry? | pass | pass | pass | yes |

The gate on out-of-corpus questions, produced by
`run_eval.py::check_out_of_scope`, cutoff 0.55. Refused 5 of 5:

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.891 | refused |

Two of the answers as produced.

**When does dropping a course start showing as a W on my transcript? (run 1)**

- Best distance: 0.2129 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_transcript_requests.txt, admin_withdrawal_deadline.txt

```
Dropping a course starts showing as a W on your transcript after week two. 

Source: admin_add_drop_deadline.txt
```

**How much does a wash cost in Fenwick Court laundry? (run 1)**

- Best distance: 0.1487 (passed the gate)
- Sources retrieved: housing_fenwick_court.txt, housing_fenwick_court_laundry.txt, housing_innisfree_hall.txt, housing_old_brewhouse.txt, housing_old_brewhouse_laundry.txt

```
A wash costs $2.00 in Fenwick Court laundry (housing_fenwick_court_laundry.txt and housing_fenwick_court.txt).
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | `judge_retrieval` found the expects phrase in a retrieved chunk for all five questions. |
| 2 | Every answer names a source | MET | All 15 answers name at least one .txt source; the wording varies between "Source: x" and parentheses, but the criterion asks that a source is named, not that it is formatted consistently, so the variation is not a failure. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused all five OUT_OF_SCOPE questions, and nothing sits near the 0.55 cutoff: in-corpus best distances ran 0.149 to 0.323, out-of-corpus 0.825 to 0.934. |
| 4 | Chunks stand on their own | MET | Exactly 7 of 8, the target to the chunk; the full reasoning is in the note below. |
| 5 | Answers stay inside the retrieved chunks | MET | No answer stated a price, time or number absent from its chunks. |

**Criterion 4: MET.** The sample was 8 chunks from `python app.py chunks -n 8`,
produced by `chunker.py::split_documents`. The command takes a fixed step
through the chunk list rather than a random draw, so the sample is
reproducible. The target was that at least 7 of the 8 chunks could answer a
question on their own, and the result was 7 of 8. The seven that passed all
open by naming their subject. The one failure is chunk 4,
`course_hist_118.txt#1`, which carries a fact but never names the course, so an
answer citing it could not say which course it applied to; the `#1` suffix
means the paragraph chunker split that document and the course name stayed in
`#0`. Worth saying plainly: 7 of 8 is exactly the target, so this verdict
turned on one chunk, and a more generous reading of "can answer a question on
their own" would have made it 8 of 8.

```
The one piece of advice: the essay rubric is posted in week 2 and it's followed exactly — read it early.
```

## Diagnoses

Nothing was missed, so there is no failure to trace to a stage. What that
means is worth saying plainly: a clean sweep on the first test points at safe
targets rather than an excellent system. What I'd Do Differently, at the end
of this file, names criterion 1 as the soft one and gives the version I would
write instead.

## The Improvement

**What I changed:** BM25 hybrid retrieval. config.py gained `HYBRID = True`,
`HYBRID_POOL = 20` and `RRF_K = 60`. `store.py::search` now pulls 20 chunks
semantically, scores that pool with BM25Okapi, and fuses the two rankings with
reciprocal rank fusion, returning the top 5 by fused score. Every Result keeps
its real Chroma distance, so gate.py is untouched, and `HYBRID = False`
reproduces the old behaviour exactly.

**Why I picked it:** My diagnosis was that retrieval finds the right document
and then fills the remaining slots with near-duplicate neighbours from other
buildings, dining halls and courses; only 1 or 2 of the 5 retrieved chunks were
on-subject on every question. BM25 matches the literal building name, which
semantic search glides past.

### Run Log — After

Source: `results/run_2026-09-28_2356_after.md`. Same table shape as the before
log, and every row is identical: all five criteria MET, 5/5 or 7/8 as before.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks stand on their own | 7 of 8 | 7/8 | n/a | n/a | MET |
| 5. Answers stay inside the retrieved chunks | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

The after run had to be repeated once. The first attempt crashed on the
fifteenth model call with a 429 from the Gemini free tier, which caps at 15
requests per minute, and run_eval.py writes its report only at the end, so
nothing was saved. The committed log is a clean single run.

Since no criterion could see the change, I took a secondary measurement:
on-subject chunks in the top 5.

| Question | Before | After |
|---|---|---|
| Fenwick laundry | 2 of 5 | 2 of 5 |
| Halden Hall | 2 of 5 | 2 of 5 |

**Did it help?**

No. On the Fenwick question, before, by rank: housing_fenwick_court_laundry,
housing_old_brewhouse, housing_fenwick_court, housing_innisfree_hall,
housing_old_brewhouse_laundry. After, by rank: housing_fenwick_court_laundry,
housing_innisfree_hall, housing_old_brewhouse, housing_fenwick_court,
admin_printing_quota. So the second Fenwick document moved down from rank 3 to
rank 4, and admin_printing_quota.txt at distance 0.7491, a chunk about $30 of
printing, entered the top 5 where it had not been before. On Halden,
housing_innisfree_hall_noise.txt replaced a dining hall document.

Why it failed: the pool is 20 of 99 chunks and the queries are short, so
common words like "cost" and "hall" match broadly. RRF weights both rankings
equally, so a chunk semantic search ranked 15th or 18th can reach the top 5 on
weak keyword overlap alone.

One thing did hold: the model did not take the bait. With the printing quota
chunk in the Fenwick top 5, all three answers still said only $2.00 and cited
only housing_fenwick_court_laundry.txt.

## What's Still Broken

**1.** No criterion measures retrieval precision. All five came out MET while
three of five retrieved chunks are off-subject. The criterion 1 rewrite in
What I'd Do Differently addresses this, but I have not tested against it.

**2.** Hybrid introduced a new risk. It can push the semantically closest
chunk out of the returned five, which changes what the gate sees. The
evidence: the Mongolia out-of-scope question's best distance moved from 0.825
before to 0.852 after. Harmless there, because it made the refusal easier, but
the same mechanism could raise an in-corpus question's best distance above the
0.55 cutoff and cause a wrong refusal.

**3.** What I would try next: shrink HYBRID_POOL from 20 to around 10, or
weight the semantic ranking above the BM25 ranking in the fusion, so a chunk
semantic search ranks poorly cannot reach the top 5 on keyword overlap alone.
Not attempted, out of time for this unit.

**4.** Criterion 4's failing chunk. course_hist_118.txt#1 still cannot name
its course. The fix would be carrying the document title into every chunk from
that document, which changes chunking, and this unit allows one change only.

## What I'd Do Differently

All five criteria came out MET on the first test, and that says at least one
target was set safe rather than the system being excellent. The soft one is
criterion 1. The target was 4 of 5 questions having the answer in the
retrieved chunks, and it came out 5 of 5. It is soft because it only asks
whether some retrieved chunk contains the fact, not whether the right document
did. On the Fenwick laundry question only 2 of the 5 retrieved chunks are
Fenwick documents, and one of the other three, housing_old_brewhouse.txt, says
"$1.50 wash", so the criterion passes anyway. The same pattern holds on all
five questions: 1 or 2 of the 5 retrieved chunks are on-subject, and the rest
are near-duplicate neighbours from other buildings, dining halls or courses.
In unit 1 I predicted the Fenwick question would fail retrieval because of the
near-identical laundry posts. It passed, but the prediction was half right:
the wrong-building chunks do come back, the model just picked correctly.

The version I would write next time: "For at least 4 of 5 questions, the
closest chunk comes from a document about the subject I asked about." That is
harder because I know it holds for the Fenwick question, where rank 1 is
housing_fenwick_court_laundry.txt, but I have not measured it for the other
four, so it is a target I could miss.
