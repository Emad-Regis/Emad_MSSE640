# Week 2: Project 1 — Triangle Classifier

**Student:** Emad Fattah

**Instructor:** Randall Granier

**Class:** MSSE640

---

## 1. Introduction

This project implements a Triangle Classifier program written in Python. The program accepts three numeric values representing the sides of a triangle and determines two things: whether the three sides form a valid triangle, and if so, what type of triangle it is — equilateral, isosceles, or scalene.

### Core Logic

Validation is based on the **triangle inequality theorem**, which states that the sum of any two sides of a triangle must be strictly greater than the third side. Classification is then determined by comparing the three sides to each other.

### Error Handling

Rather than allowing the program to crash on bad input, two custom exception classes were created:

- **`InvalidSideError`** — raised when any side is zero, negative, or a boolean value. Booleans (`True`/`False`) required special handling because Python internally treats them as subclasses of integers, meaning `True` would silently pass as `1` and `False` as `0` without an explicit check.
- **`InvalidTriangleError`** — raised when the three sides are all positive numbers but fail the triangle inequality theorem (e.g. sides 1, 2, 10).
- Python's built-in **`TypeError`** — raised when a side is not a number at all, such as a string, `None`, or a list.

These exceptions allow the program to display a clear, meaningful error message and continue running rather than terminating unexpectedly.

### Unit Tests

Unit tests were written using Python's built-in `unittest` library, organized into 8 test classes covering 41 individual tests. Tests were chosen to cover valid triangles, all three classification types, every rainy-day input scenario, and all possible orderings of side inputs to ensure the result is order-independent.

---

## 2. Details of the Program

### IDE

The program was developed using **Jupyter notebook**, an IDE that supports Python and already installed in a local Macbook. The environment uses **Python 3.14.5** and the standard library's `unittest` module for testing.

### How Data Enters the Program

The program supports two input modes:

1. **Interactive CLI (`main()` function)** — The user is prompted to enter each of the three sides one at a time via the terminal. The program loops continuously, accepting new sets of sides after each result or error, and exits when the user types `q`.

2. **Direct function calls (for testing and Jupyter)** — The core function `classify_triangle(a, b, c)` can be imported and called directly with values. This is how all unit tests supply data, and it is also the recommended approach for use in Jupyter Notebook.

No data was read from a file, and no results were written to a file. The program is self-contained and outputs results directly to the notebook cell.

### Output

Results are printed to the console in the following format:

```
Valid triangle? Yes
Triangle type:  Scalene
```

Errors print a descriptive message and the program continues:

```
Error: Side a must be greater than zero (got 0.0).
```

---

## 3. Table of Example Test Data

| Side A  | Side B | Side C | Valid?  | Type / Error                                    |
|---------|--------|--------|---------|-------------------------------------------------|
| 3       | 4      | 5      | ✅ Yes  | Scalene                                         |
| 5       | 5      | 5      | ✅ Yes  | Equilateral                                     |
| 5       | 5      | 8      | ✅ Yes  | Isosceles                                       |
| 6       | 6      | 9      | ✅ Yes  | Isosceles                                       |
| 7       | 11     | 13     | ✅ Yes  | Scalene                                         |
| 2.5     | 2.5    | 2.5    | ✅ Yes  | Equilateral                                     |
| 1.5     | 1.5    | 2.0    | ✅ Yes  | Isosceles                                       |
| 0       | 4      | 5      | ❌ No   | `InvalidSideError` — side is zero               |
| -1      | 4      | 5      | ❌ No   | `InvalidSideError` — side is negative           |
| 1       | 2      | 3      | ❌ No   | `InvalidTriangleError` — degenerate flat triangle |
| 1       | 2      | 10     | ❌ No   | `InvalidTriangleError` — inequality violated    |
| 10      | 3      | 4      | ❌ No   | `InvalidTriangleError` — inequality violated    |
| `"abc"` | 4      | 5      | ❌ No   | `TypeError` — side is not a number              |
| `None`  | 4      | 5      | ❌ No   | `TypeError` — side is not a number              |
| `True`  | 4      | 5      | ❌ No   | `TypeError` — boolean is not a valid side       |
| `False` | 3      | 5      | ❌ No   | `TypeError` — boolean is not a valid side       |
| 0.0     | 4      | 5      | ❌ No   | `InvalidSideError` — float zero is still zero   |

---

## 4. Unit Tests

### Test Classes and Rationale

**`TestValidTriangle`** *(4 tests)*
Confirms that a basic valid scalene, equilateral, and isosceles triangle all return `valid: True`. This is the most fundamental check — if valid triangles are rejected, nothing else matters.

**`TestTriangleType`** *(8 tests)*
Verifies the correct type label is returned for each triangle family, including float inputs and all three isosceles orientations (a=b, b=c, a=c). This ensures classification does not depend on which pair of equal sides happens to be passed first.

**`TestInvalidSides`** *(13 tests)*
Covers every category of bad side input: zero (each position), negative (each position), all zeros, string, `None`, list, and booleans (`True`, `False`, all three booleans). Each test confirms the correct exception type is raised. Booleans were added as a separate group because they are a non-obvious failure mode.

**`TestTriangleInequality`** *(5 tests)*
Tests triangles where the sides are all positive but still invalid — including the degenerate edge case where two sides sum to exactly the third (1+2=3), and cases where each of the three sides is individually too large.

**`TestScalenePermutations`** *(3 tests)*
Uses Python's `itertools.permutations` to test all 6 orderings of the sides (3,4,5) and (7,11,13). This ensures the classification algorithm does not depend on the order in which sides are provided.

**`TestIsoscelesPermutations`** *(1 test)*
All orderings of (5,5,8) — ensures isosceles is detected regardless of where the equal sides appear in the argument list.

**`TestEquilateralPermutations`** *(1 test)*
All orderings of (6,6,6) — confirms equilateral detection is consistent (since all permutations of an equilateral triangle are identical, this also serves as a symmetry sanity check).

**`TestZeroSidePermutations`** *(1 test)*
All orderings of (0,4,5) — confirms that a zero side is caught regardless of whether it appears as argument `a`, `b`, or `c`.

**`TestEdgeCases`** *(5 tests)*
Boundary values: very small floats (0.001), very large numbers (1,000,000), float zero (0.0), float isosceles, and a check that the result dictionary returns the correct sides tuple.

---

## 5. Bugs Encountered During Testing

### Bug 1 — Booleans Accepted as Valid Sides

**Description:** When `True` or `False` was passed as a side, the program accepted them silently. `True` was treated as `1` and `False` as `0`, meaning `classify_triangle(True, True, True)` returned `equilateral` instead of raising an error.

**Root Cause:** Python's `bool` type is a subclass of `int`. The original type check `isinstance(value, (int, float))` returned `True` for booleans because they technically are integers.

**Fix:** An explicit boolean check was added before the numeric check:

```python
if isinstance(value, bool) or not isinstance(value, (int, float)):
    raise TypeError(...)
```

This catches booleans first and rejects them before the `int/float` check runs.

---

### Bug 2 — Import Failure When Tests Run from Different Directories

**Description:** Running `python3 -m unittest test_triangle` from inside the `triangle/` folder worked, but running from the workspace root caused an `ImportError` because the `triangle` package could not be located.

**Root Cause:** The test file used `from triangle import ...`, which requires the workspace root to be on `sys.path`. The root is not added automatically when the runner is invoked from a different directory.

**Fix:** Two changes were made:

1. A `__init__.py` file was added to `triangle/` to make it a proper Python package.
2. The test file inserts the workspace root into `sys.path` at the top, so imports resolve correctly regardless of where the test runner is invoked from:

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

## 6. Problems Encountered

### Problem 1 — Interactive Input Cannot Be Tested Automatically

The `main()` function relies on `input()`, which pauses execution and waits for keyboard input. This makes it impossible to test through standard unit tests. This was resolved by separating the core logic (`classify_triangle`, `validate_sides`) from the CLI layer (`main()`), so all logic could be tested by calling functions directly, while the interactive interface was tested manually.

### Problem 2 — Degenerate Triangle Edge Case

A triangle where two sides sum to exactly the third (e.g. 1, 2, 3) is geometrically a straight line, not a real triangle. The inequality check needed to use strict greater-than (`>`) rather than greater-than-or-equal (`>=`) to correctly reject these degenerate cases. Using `<=` instead of `<` in the condition caught this correctly:

```python
if a + b <= c or a + c <= b or b + c <= a:
    raise InvalidTriangleError(...)
```
---

### 7. Codes 

[1.Project1_Tringle(1)](https://github.com/Emad-Regis/Emad_MSSE640/blob/main/Code/1.Project1_Traingle.py)

---

### 8. Run it interactively using GitHub Codespaces (Cloud IDE) 

Run it interactively using GitHub Codespaces (Cloud IDE)
If you want to edit and test your Python script inside a virtual web-based editor (VS Code inside your browser), you can use GitHub Codespaces:

1. Go to your GitHub repository page.

![pic1](/Assignments/Images/Project_1_Traingles_Classifier/1.Opengitub.png)

2. Click the green Code button in the upper-right corner.
3. Select the Codespaces tab and click Create codespace on main.
4. A full VS Code interface will load in your browser. Open the built-in terminal at the bottom and type the values of the traingle's sides. 

