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

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
