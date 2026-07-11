"""
Student: Emad Fattah 

Instructor: Randall Granier
MSSE-640

Project # 1 
Triangle validator and classifier.

Given three side lengths, determines:
 - Whether the sides form a valid triangle
 - The type: equilateral, isosceles, or scalene

Custom exceptions are raised for bad inputs (negative, zero, or
non-numeric sides) so callers can handle them clearly.
"""


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class InvalidSideError(ValueError):
   """Raised when one or more sides have an invalid length (≤ 0)."""


class InvalidTriangleError(ValueError):
   """Raised when the three sides do not form a valid triangle."""


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def validate_sides(a: float, b: float, c: float) -> None:
   for name, value in (("a", a), ("b", b), ("c", c)):
       # bool is a subclass of int in Python, but True/False are not valid sides
       if isinstance(value, bool) or not isinstance(value, (int, float)):
           raise TypeError(
               f"Side {name} must be a numeric value, got {type(value).__name__!r}."
           )
       if value <= 0:
           raise InvalidSideError(
               f"Side {name} must be greater than zero (got {value})."
           )

   if a + b <= c or a + c <= b or b + c <= a:
       raise InvalidTriangleError(
           f"Sides {a}, {b}, {c} do not satisfy the triangle inequality "
           "(the sum of any two sides must exceed the third)."
       )


def triangle_type(a: float, b: float, c: float) -> str:
   if a == b == c:
       return "equilateral"
   if a == b or b == c or a == c:
       return "isosceles"
   return "scalene"


def classify_triangle(a: float, b: float, c: float) -> dict:
   validate_sides(a, b, c)
   return {
       "valid": True,
       "type": triangle_type(a, b, c),
       "sides": (a, b, c),
   }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_side(raw: str, label: str) -> float:
   try:
       return float(raw.strip())
   except ValueError:
       raise TypeError(f"Side {label} must be a number; {raw!r} is not valid.")


def main() -> None:
   print("=== Triangle Classifier ===")
   print("Enter the three side lengths (or 'q' to quit).\n")

   while True:
       try:
           raw_a = input("Side a: ")
           if raw_a.strip().lower() == "q":
               break
           raw_b = input("Side b: ")
           if raw_b.strip().lower() == "q":
               break
           raw_c = input("Side c: ")
           if raw_c.strip().lower() == "q":
               break

           a = _parse_side(raw_a, "a")
           b = _parse_side(raw_b, "b")
           c = _parse_side(raw_c, "c")

           result = classify_triangle(a, b, c)
           print(f"\nValid triangle? Yes")
           print(f"Triangle type:  {result['type'].capitalize()}\n")

       except (TypeError, InvalidSideError, InvalidTriangleError) as exc:
           print(f"\nError: {exc}\n")
       except EOFError:
           break


if __name__ == "__main__":
   main()
