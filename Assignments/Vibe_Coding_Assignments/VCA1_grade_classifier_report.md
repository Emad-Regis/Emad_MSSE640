



# Boundary Value Analysis & Equivalence Class Partitioning
## A Comprehensive Report — Student Grade Classifier

**Student:** Emad Fattah

**Instructor:** Randall Granier

**Class:** MSSE640

**Vibe Coding Assignment 1**

---
**Course:** Software Quality Assurance  
**Date:** July 15, 2026  
**Tools Used:** Python 3.11, Streamlit, pytest, Replit AI Agent

---

## Table of Contents

1. [Introduction](#introduction)
2. [Testing Methodology](#methodology)
3. [Sample Python Application](#sample-app)
4. [Sunny Day Scenarios](#sunny-day)
5. [Rainy Day Scenarios](#rainy-day)
6. [Test Results](#test-results)
7. [Conclusion](#conclusion)
8. [What I Learned About AI Tools](#ai-learned)

---

## 1. Introduction <a name="introduction"></a>

Software testing is the discipline of verifying that a program behaves correctly across all meaningful inputs — not just the convenient ones. Two of the most effective and widely taught black-box test-design techniques are **Equivalence Class Partitioning (ECP)** and **Boundary Value Analysis (BVA)**. This report documents the design, implementation, and testing of a Student Grade Classifier application in Python that applies both techniques to a realistic grading problem.

### The Problem

A university system must convert a raw integer score (0–100) into a standard letter grade (F through A+) along with its corresponding GPA point value. The system must:

- Accept any integer input, including values outside the 0–100 range
- Return a letter grade and GPA for all valid scores
- Return `Invalid` (with no GPA) for any score below 0 or above 100
- Correctly handle the exact boundaries between adjacent grade classes

This problem is ideal for demonstrating ECP and BVA because it has a well-defined input domain, clear equivalence partitions, numerous adjacent boundaries, and an `Invalid` domain on both ends — all of which are common patterns in real production systems.

### Why These Techniques Matter

Testing every possible integer score from −∞ to +∞ is impossible. Even restricting to 0–100 yields 101 inputs. ECP reduces this to **13 representative tests** by recognising that every value inside a class exercises the same code path. BVA then adds **targeted boundary probes** — the values at and just across each class boundary — because fence-post errors (`>` instead of `>=`, for example) are among the most common and invisible bugs in range-based logic.

Together, these two techniques deliver thorough coverage with a minimal, well-reasoned test suite.

---

## 2. Testing Methodology <a name="methodology"></a>

### Equivalence Class Partitioning (ECP)

ECP divides the entire input domain into groups (partitions) such that every value within a group is expected to produce the same output. The classifier recognises 15 partitions:

| Class | Range    | Grade   | GPA |
|-------|----------|---------|-----|
| 1     | < 0      | Invalid | —   |
| 2     | 0–59     | F       | 0.0 |
| 3     | 60–62    | D−      | 0.7 |
| 4     | 63–66    | D       | 1.0 |
| 5     | 67–69    | D+      | 1.3 |
| 6     | 70–72    | C−      | 1.7 |
| 7     | 73–76    | C       | 2.0 |
| 8     | 77–79    | C+      | 2.3 |
| 9     | 80–82    | B−      | 2.7 |
| 10    | 83–86    | B       | 3.0 |
| 11    | 87–89    | B+      | 3.3 |
| 12    | 90–92    | A−      | 3.7 |
| 13    | 93–96    | A       | 3.9 |
| 14    | 97–100   | A+      | 4.0 |
| 15    | > 100    | Invalid | —   |

ECP test strategy: select **one interior value** from each valid class (Classes 2–14). If one interior value works correctly, all values in that class are assumed correct — because they all follow the same code path.

### Boundary Value Analysis (BVA)

BVA augments ECP by probing the four values around each class boundary:

| Probe   | Meaning                                      |
|---------|----------------------------------------------|
| Min − 1 | Just below the lower bound — belongs to the previous class |
| Min ▶   | Exact lower bound — must be included in this class |
| ◀ Max   | Exact upper bound — must be included in this class |
| Max + 1 | Just above the upper bound — belongs to the next class |

For the class B (83–86), the four BVA probes are: **82, 83, 86, 87**. Testing both 82 and 83 confirms the lower fence-post; testing both 86 and 87 confirms the upper fence-post. A bug such as writing `score > 83` instead of `score >= 83` would silently misclassify every student with exactly 83 points — BVA makes that invisible fence-post an explicit test target.

### Sunny Day vs. Rainy Day

| Category  | Input Profile                             | What It Verifies |
|-----------|-------------------------------------------|------------------|
| Sunny Day | Interior values, well inside valid ranges | Normal operation; the happy path |
| Rainy Day | Exact boundaries, Invalid domain (< 0, > 100) | Edge behaviour; off-by-one guards; error handling |

---

## 3. Sample Python Application <a name="sample-app"></a>

The application is structured as three independent files so that the core logic can be tested without any UI dependency.

```
grade-classifier-python/
├── grade_utils.py            ← data model + classifier (no UI imports)
├── app.py                    ← Streamlit UI (imports grade_utils)
└── test_grade_classifier.py  ← pytest suite (imports grade_utils)
```

### 3.1 Core Logic — `grade_utils.py`

The data model uses a frozen dataclass so each class definition is immutable and hashable. The classifier iterates the table and returns the first matching partition — covering −∞ to +∞ because the two Invalid sentinels have unbounded ends (`bva_min = None` and `bva_max = None` respectively).

```python
"""
grade_utils.py
==============
Core classification logic shared by the Streamlit UI and the test suite.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BvaClass:
    id: int
    range_label: str
    bva_min: Optional[int]   # None = no lower bound (−∞)
    bva_max: Optional[int]   # None = no upper bound (+∞)
    grade: str
    gpa: Optional[float]     # None for Invalid classes
    theme: str               # UI colour key


BVA_CLASSES: list[BvaClass] = [
    BvaClass(1,  "< 0",    None, -1,  "Invalid", None, "gray"),
    BvaClass(2,  "0–59",   0,    59,  "F",       0.0,  "red"),
    BvaClass(3,  "60–62",  60,   62,  "D-",      0.7,  "orange"),
    BvaClass(4,  "63–66",  63,   66,  "D",       1.0,  "orange"),
    BvaClass(5,  "67–69",  67,   69,  "D+",      1.3,  "orange"),
    BvaClass(6,  "70–72",  70,   72,  "C-",      1.7,  "yellow"),
    BvaClass(7,  "73–76",  73,   76,  "C",       2.0,  "yellow"),
    BvaClass(8,  "77–79",  77,   79,  "C+",      2.3,  "yellow"),
    BvaClass(9,  "80–82",  80,   82,  "B-",      2.7,  "teal"),
    BvaClass(10, "83–86",  83,   86,  "B",       3.0,  "teal"),
    BvaClass(11, "87–89",  87,   89,  "B+",      3.3,  "teal"),
    BvaClass(12, "90–92",  90,   92,  "A-",      3.7,  "indigo"),
    BvaClass(13, "93–96",  93,   96,  "A",       3.9,  "indigo"),
    BvaClass(14, "97–100", 97,   100, "A+",      4.0,  "indigo"),
    BvaClass(15, "> 100",  101,  None,"Invalid", None, "gray"),
]


def classify_score(score: int) -> BvaClass:
    """
    Map an integer score to its equivalence class.

    ECP logic: find the first partition whose [bva_min, bva_max] range
    contains the score. The table covers −∞ to +∞, so this always returns
    a class — no score can fall through.
    """
    for cls in BVA_CLASSES:
        below = cls.bva_min is None or score >= cls.bva_min
        above = cls.bva_max is None or score <= cls.bva_max
        if below and above:
            return cls
    raise ValueError(f"No equivalence class found for score {score}")


def bva_points(cls: BvaClass) -> dict:
    """
    Return the four standard BVA probes for a class:
      min_minus_1  — just below the lower boundary
      min          — exact lower boundary
      max          — exact upper boundary
      max_plus_1   — just above the upper boundary
    None indicates an unbounded end.
    """
    return {
        "min_minus_1": cls.bva_min - 1 if cls.bva_min is not None else None,
        "min":         cls.bva_min,
        "max":         cls.bva_max,
        "max_plus_1":  cls.bva_max + 1 if cls.bva_max is not None else None,
    }
```

### 3.2 Streamlit UI — `app.py`

The Streamlit app (`app.py`) provides five tabs: an App Overview explaining the methodology, an Interactive Demo where users type any score and see the grade, GPA, equivalence class, and live BVA boundary points, a Sunny Day tab, a Rainy Day tab, and an inline Unit Test runner that executes every assertion in the Streamlit process itself and reports Pass/Fail without needing a separate terminal.

The live code-path panel in the Interactive Demo tab shows exactly which branch was taken for the current score:

```python
# Example output when score = 85:
# Running: classify_score(85)

for cls in BVA_CLASSES:
    below = cls.bva_min is None or 85 >= cls.bva_min
    above = cls.bva_max is None or 85 <= cls.bva_max
    if below and above:
        return cls   # ← matched class 10: "83–86" → B
```

---

## 4. Sunny Day Scenarios <a name="sunny-day"></a>

Sunny Day tests verify the **normal, expected path**: every score is chosen from the interior of its equivalence class, well away from any boundary. ECP guarantees that if the interior value passes, every other value in that class will also pass.

### Test Pattern

```python
@pytest.mark.parametrize(
    "score,expected_grade,expected_gpa",
    SUNNY_DAY_CASES,
    ids=[f"score={s}" for s, _, _ in SUNNY_DAY_CASES],
)
def test_sunny_day_grade(score, expected_grade, expected_gpa):
    """Interior class representative yields the correct letter grade."""
    result = classify_score(score)
    assert result.grade == expected_grade, (
        f"Score {score}: expected grade {expected_grade!r}, got {result.grade!r}"
    )


@pytest.mark.parametrize(
    "score,expected_grade,expected_gpa",
    SUNNY_DAY_CASES,
    ids=[f"score={s}" for s, _, _ in SUNNY_DAY_CASES],
)
def test_sunny_day_gpa(score, expected_grade, expected_gpa):
    """Interior class representative yields the correct GPA."""
    result = classify_score(score)
    assert result.gpa == pytest.approx(expected_gpa), (
        f"Score {score}: expected GPA {expected_gpa}, got {result.gpa}"
    )
```

### Sunny Day Test Cases

| Score | Class Range | Expected Grade | Expected GPA | Result |
|-------|-------------|----------------|--------------|--------|
| 30    | 0–59        | F              | 0.0          | ✅ PASS |
| 61    | 60–62       | D−             | 0.7          | ✅ PASS |
| 64    | 63–66       | D              | 1.0          | ✅ PASS |
| 68    | 67–69       | D+             | 1.3          | ✅ PASS |
| 71    | 70–72       | C−             | 1.7          | ✅ PASS |
| 74    | 73–76       | C              | 2.0          | ✅ PASS |
| 78    | 77–79       | C+             | 2.3          | ✅ PASS |
| 81    | 80–82       | B−             | 2.7          | ✅ PASS |
| 85    | 83–86       | B              | 3.0          | ✅ PASS |
| 88    | 87–89       | B+             | 3.3          | ✅ PASS |
| 91    | 90–92       | A−             | 3.7          | ✅ PASS |
| 95    | 93–96       | A              | 3.9          | ✅ PASS |
| 99    | 97–100      | A+             | 4.0          | ✅ PASS |

**All 13 × 2 = 26 Sunny Day assertions passed.**

> **Why interior values?**  
> If the class covering 83–86 passes with score 85, it will also pass with 84 and 86 — they all follow the same code path. ECP reduces the 101-value valid domain (0–100) down to 13 representative tests without sacrificing meaningful coverage.

---

## 5. Rainy Day Scenarios <a name="rainy-day"></a>

Rainy Day tests target the two locations where bugs cluster most densely: exact boundary values between adjacent grades, and the invalid domain outside 0–100.

### Test Pattern

```python
@pytest.mark.parametrize(
    "score,expected_grade,why",
    RAINY_DAY_CASES,
    ids=[f"score={s}" for s, _, _ in RAINY_DAY_CASES],
)
def test_rainy_day_grade(score, expected_grade, why):
    """Boundary / invalid input returns the correct grade (or Invalid)."""
    result = classify_score(score)
    assert result.grade == expected_grade, (
        f"Score {score} [{why}]: expected {expected_grade!r}, got {result.grade!r}"
    )


@pytest.mark.parametrize(
    "score,expected_grade,why",
    [(s, g, w) for s, g, w in RAINY_DAY_CASES if g == "Invalid"],
    ids=[f"score={s}" for s, g, _ in RAINY_DAY_CASES if g == "Invalid"],
)
def test_rainy_day_invalid_has_no_gpa(score, expected_grade, why):
    """Invalid-class results must always carry gpa=None."""
    result = classify_score(score)
    assert result.gpa is None, (
        f"Score {score}: Invalid class must have gpa=None, got {result.gpa}"
    )
```

### Rainy Day Test Cases

| Score | Test Point         | Expected Grade | Why It Matters                                      | Result  |
|-------|--------------------|----------------|-----------------------------------------------------|---------|
| −1    | Invalid domain     | Invalid        | One below absolute minimum — lower-bound guard      | ✅ PASS |
| −50   | Invalid domain     | Invalid        | Deeply negative — invalid domain                    | ✅ PASS |
| 0     | Absolute boundary  | F              | Absolute minimum — must not be Invalid              | ✅ PASS |
| 59    | BVA fence-post     | F              | Max of F class — last failing score                 | ✅ PASS |
| 60    | BVA fence-post     | D−             | Min of D− class — first passing score (F↔D− fence) | ✅ PASS |
| 62    | BVA fence-post     | D−             | Max of D− class — last D−; next must be D           | ✅ PASS |
| 63    | BVA fence-post     | D              | Min of D class — fence-post D−↔D                   | ✅ PASS |
| 82    | BVA fence-post     | B−             | Max of B− class — fence-post B−↔B                  | ✅ PASS |
| 83    | BVA fence-post     | B              | Min of B class — fence-post B−↔B                   | ✅ PASS |
| 96    | BVA fence-post     | A              | Max of A class — fence-post A↔A+                   | ✅ PASS |
| 97    | BVA fence-post     | A+             | Min of A+ class — fence-post A↔A+                  | ✅ PASS |
| 100   | Absolute boundary  | A+             | Absolute maximum — must not be Invalid              | ✅ PASS |
| 101   | Invalid domain     | Invalid        | One above absolute maximum — upper-bound guard      | ✅ PASS |
| 200   | Invalid domain     | Invalid        | Far above maximum — invalid domain                  | ✅ PASS |

**All 14 Rainy Day grade assertions and 4 Invalid-GPA assertions passed.**

### BVA Cross-Boundary Probes

An additional 12 parametrized tests verify that every pair of adjacent class boundaries holds correctly. Each test checks both the Max of class N and the Min of class N+1 in a single assertion:

```python
@pytest.mark.parametrize(
    "low_score,low_grade,high_score,high_grade",
    [
        (59, "F",  60, "D-"),   # F ↔ D-
        (62, "D-", 63, "D"),    # D- ↔ D
        (66, "D",  67, "D+"),   # D ↔ D+
        (69, "D+", 70, "C-"),   # D+ ↔ C-
        (72, "C-", 73, "C"),    # C- ↔ C
        (76, "C",  77, "C+"),   # C ↔ C+
        (79, "C+", 80, "B-"),   # C+ ↔ B-
        (82, "B-", 83, "B"),    # B- ↔ B
        (86, "B",  87, "B+"),   # B ↔ B+
        (89, "B+", 90, "A-"),   # B+ ↔ A-
        (92, "A-", 93, "A"),    # A- ↔ A
        (96, "A",  97, "A+"),   # A ↔ A+
    ],
    ids=["F↔D-","D-↔D","D↔D+","D+↔C-","C-↔C","C↔C+",
         "C+↔B-","B-↔B","B↔B+","B+↔A-","A-↔A","A↔A+"],
)
def test_cross_boundary(low_score, low_grade, high_score, high_grade):
    assert classify_score(low_score).grade  == low_grade
    assert classify_score(high_score).grade == high_grade
```

All 12 × 2 = 24 cross-boundary assertions passed.

---

## 6. Test Results Summary <a name="test-results"></a>

```
$ pytest artifacts/grade-classifier-python/test_grade_classifier.py -v

collected 58 items

PASSED test_sunny_day_grade[score=30]
PASSED test_sunny_day_grade[score=61]
... (13 tests)
PASSED test_sunny_day_gpa[score=30]
... (13 tests)
PASSED test_rainy_day_grade[score=-1]
... (14 tests)
PASSED test_rainy_day_invalid_has_no_gpa[score=-1]
... (4 tests)
PASSED test_cross_boundary[F↔D-]
... (12 tests)
PASSED test_score_zero_is_f
PASSED test_score_100_is_a_plus

============ 58 passed in 0.09s ============
```

| Suite                        | Tests | Passed | Failed |
|------------------------------|-------|--------|--------|
| Sunny Day — grade            | 13    | 13     | 0      |
| Sunny Day — GPA              | 13    | 13     | 0      |
| Rainy Day — grade            | 14    | 14     | 0      |
| Rainy Day — Invalid has no GPA | 4   | 4      | 0      |
| Cross-boundary BVA probes    | 12    | 12     | 0      |
| Absolute bounds (0 and 100)  | 2     | 2      | 0      |
| **Total**                    | **58**| **58** | **0**  |

---

## 7. Conclusion <a name="conclusion"></a>

### Problems Encountered

**Preview pane routing conflict**  
The most significant technical obstacle was that the Replit preview pane uses path-based routing — the React app holds the root path (`/`), so the Streamlit app running on port 8080 was invisible in the browser UI. Every screenshot attempt via the standard external-URL tool returned the React app instead of the Python app. The workaround was to invoke Playwright Chromium directly against `localhost:8080`, which required knowing that `$REPLIT_PLAYWRIGHT_CHROMIUM_EXECUTABLE` was available as an environment variable. This is not documented prominently; discovering it required trial and error across multiple approaches.

**Streamlit is not a registered artifact type**  
Replit's artifact system supports `web`, `api`, and `design` types. Streamlit fits none of these, which meant the Python app could not receive a proxy path, automatic workflow generation, or preview-pane routing. Both the workflow and the port binding had to be configured manually. Any student or developer expecting a one-click deployment of a Streamlit app would hit this limitation without warning.

**Keeping two codebases in sync**  
The grade logic had to remain identical in both TypeScript (`gradeUtils.ts` for the React app) and Python (`grade_utils.py` for the Streamlit app). There was no code generation or shared source of truth between the two runtimes. Every change to the boundary table — for example, adjusting where D− begins and ends — required updates in two files and independent verification in two test suites. This is a fragile pattern at scale and would be better solved by a shared JSON configuration file consumed by both apps at startup.

**Off-by-one fence-post decisions at design time**  
Before a single line of code could be written, every grade boundary had to be decided precisely. Does score 90 belong to A− or A? Exactly which score is the first passing grade? These questions seem simple but require explicit answers that the classifier logic depends on entirely. Getting them wrong silently — for example, using `>` instead of `>=` in the lower-bound comparison — produces a misclassification that affects all students at that exact boundary value and is invisible without BVA test cases targeting that specific point.

### Key Takeaways

BVA and ECP together are more powerful than either technique alone. ECP reduces the test space to a manageable number of representatives; BVA then drills into exactly the points ECP intentionally skips — the edges. The 59/60 fence-post is the clearest illustration: both values are "close to passing," but one is F and one is D−. A single wrong comparison operator would silently produce the wrong grade for every student who scores exactly 59 or 60. BVA makes that invisible risk an explicit, named test case.

The effort to write a comprehensive test suite upfront pays off immediately. When the classifier was first implemented, all 58 tests passed on the first run because the boundary table was specified before the code was written. That test-first discipline prevented the ambiguous-boundary problem from becoming a hidden bug.

---

## 8. What I Learned About AI Tools <a name="ai-learned"></a>

### The AI is a strong first-draft partner, not a passive executor

When asked to "build a BVA demo," the AI did not produce a trivial score-to-grade lookup dictionary. It structured the problem into formally defined equivalence classes, extracted reusable utility modules so the UI and test suite could share one source of truth, generated parametrized test cases with meaningful IDs, and separated concerns — data model, classifier, UI, tests — into independent files. This mirrors how an experienced engineer would approach the problem, not how a script following a prompt would.

### It surfaces implicit decisions and forces clarity

Several choices that had not been consciously made were surfaced during implementation: whether out-of-range scores should return `"Invalid"` or raise an exception; whether GPA should be `None` or `0.0` for invalid inputs; whether the BVA table should use `None` sentinels to represent open-ended boundaries, or use large integers like `−9999` and `9999`. Each of these was identified, a recommendation was made with reasoning, and the decision was encoded in the data model. The AI treated ambiguous design points as design questions rather than assumptions — which is the correct behaviour for a senior engineer.

### It handles repetitive accuracy without fatigue

Writing 58 parametrized pytest test cases that cover every equivalence class boundary pair, mirroring 68 Vitest test cases in a completely different language, keeping column names and expected values consistent across two codebases, and generating inline code-path explanations for every input value are tasks where human attention drifts and typos accumulate. The AI produced these consistently and correctly. Spot-checking against the boundary table revealed zero discrepancies.

### Knowing the environment limits matters as much as knowing the tools

The AI was only as effective as its understanding of the Replit environment. The preview routing issue, the artifact type constraint, and the Playwright workaround all required platform-specific knowledge. When that knowledge was available in context, the AI applied it correctly and found the right workaround immediately. When the limitation appeared without prior context, the AI made plausible but incorrect assumptions — for instance, attempting to take a screenshot via an external URL that pointed to the wrong port. The lesson is that AI tools amplify what the user knows about their environment. They do not replace environmental understanding; they accelerate applying it.

### Iteration speed changes the design conversation

Because the AI could implement a working version of each feature — the interactive demo, the cross-boundary probe table, the inline test runner — in minutes rather than hours, it became practical to try an approach, evaluate it visually, and change direction without significant cost. The slider was added and then removed based on user feedback within a single session. The inline test runner was added because it was cheap to implement, even though the standalone pytest file already existed. This faster feedback loop changes how design decisions get made: instead of committing to an approach based on a specification, it becomes possible to build, look, and decide.

### AI-generated code still requires human review at boundaries

The AI consistently produced code that was syntactically correct and logically structured. However, the specific numeric boundaries in the grade table — 60, 63, 67, 70, 73, 77, 80, 83, 87, 90, 93, 97 — were domain decisions, not derivable from any general principle. The AI encoded whatever boundaries it was given. If the specification had been ambiguous (for example, "D− covers the low-60s") and no explicit table was provided, the AI would have had to infer numbers — and those inferences would have required careful human verification. For any application where the boundary values carry real-world consequence (grading, financial thresholds, medical dosage ranges), the human role is to specify those values precisely and then use tools like BVA to verify that the code implements them exactly as specified.

---
## Run Exmample 
[Fige_1]![_

---
### Run in Replit ###

click on link below 

![Run on Replit]](https://replit.com/@efattah/Grade-Classifier/task/a69e8fc6-5514-4eba-98ec-c16a22f529df?settings.tab=integrations)

*End of Report*
