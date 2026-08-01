# E-Check Payment Simulator
## Decision Table Test Methodology 
 
**Language / Framework:** Python 3 · Streamlit 

**Date:** August 01, 2026

**Student:** Emad Fattah

**Instructor:** Randall Granier


**Class:** MSSE640

**Vibe Coding Assignment 2**

**Course:** Software Quality Assurance 

---

## 1. Introduction

Electronic check (e-check) processing requires that a submission pass a fixed set of underwriting rules before it can be queued for settlement. A missed rule — a mistyped routing number, a blank name field, a zero-dollar amount — means the payment fails to clear. The challenge for testers is making sure every rule is tested independently, and that combinations of failures are also surfaced correctly.

This report describes the **Decision Table Testing** methodology applied to that problem, explains when the technique is the right tool and when it is not, demonstrates a working Python application that embodies the methodology, and then executes both a Sunny Day (all rules satisfied) and three Rainy Day (one or more rules violated) scenarios to confirm the system behaves correctly in each case.

### What Is Decision Table Testing?

Decision table testing is a **black-box technique** that maps every meaningful combination of input conditions to its expected output. Each column of the table is one test case. Each row is one condition (rule). The cell at the intersection is either True/False or a specific input value. The bottom rows record the expected action or outcome.

The approach was developed in the 1960s for business rule verification and remains the standard technique wherever a system's behaviour is driven by a set of mutually evaluated boolean conditions — precisely the shape of an e-check underwriting engine.

For the nine-rule e-check simulator the table takes this simplified form:

| Condition | TC-01 | TC-02 | TC-08 | TC-11 |
|-----------|:-----:|:-----:|:-----:|:-----:|
| First name present | ✓ | ✓ | **✗** | ✓ |
| Last name present | ✓ | ✓ | ✓ | ✓ |
| Street address present | ✓ | ✓ | ✓ | ✓ |
| Valid state selected | ✓ | ✓ | ✓ | ✓ |
| ZIP = 5 digits | ✓ | ✓ | ✓ | **✗** |
| Phone = 10 digits | ✓ | ✓ | ✓ | ✓ |
| Routing = 9 digits | ✓ | **✗** | ✓ | ✓ |
| Account = 8–12 digits | ✓ | ✓ | ✓ | **✗** |
| Amount > $0.00 | ✓ | ✓ | ✓ | **✗** |
| **Expected verdict** | **APPROVED** | **DECLINED** | **DECLINED** | **DECLINED** |

Each column is a self-contained scenario that can be executed against the live application, a unit test, or a command-line script.

---

## 2. When to Use Decision Table Testing

Decision table testing is the right choice when **all of the following are true**:

### 2.1 The System Has Discrete, Boolean Conditions
Each rule evaluates to either satisfied or violated — there is no continuous probability, no fuzzy logic. The routing-number rule is either `True` or `False`; there is no "mostly correct" routing number. This is the single most important prerequisite. If the conditions involve ranges, thresholds, or floating-point tolerances, a different technique (boundary-value analysis, equivalence partitioning) should be layered on top.

### 2.2 Rules Are Evaluated Simultaneously and Conjunctively
The payment is approved only when *all* nine rules pass. If any one fails, the verdict is declined and *all* failing rules are reported. This conjunctive, parallel structure is exactly what decision tables are designed for. In contrast, a sequential system where the output of step 1 feeds into step 2 calls for state-transition or cause-effect testing instead.

### 2.3 Requirements Are Stable and Well-Defined
Building a decision table requires knowing, in advance, exactly what each condition is and exactly what the expected output is for every combination. For the e-check simulator the requirements come from banking settlement standards — they are precise, externally mandated, and unlikely to change weekly. If the rules are still evolving, the table must be redrawn every time a rule changes, which adds overhead without equivalent benefit.

### 2.4 The Number of Conditions Is Manageable
A complete decision table for *n* binary conditions has 2ⁿ columns. Nine rules produce 512 theoretically possible combinations. In practice, many combinations are dominated or infeasible (no realistic payment has an invalid first name and a valid first name simultaneously), so the table is collapsed to a representative subset — the approach used here with four test cases. Still, the technique becomes unwieldy above approximately 15 conditions.

### 2.5 You Need Traceability Between Requirements and Tests
Each row of the table maps directly to one requirement. Each column maps directly to one test case. This one-to-one traceability is valuable during audits and code reviews — a reviewer can confirm instantly which test exercises which rule.

---

## 3. Limitations

### 3.1 Combinatorial Explosion
The full decision table for nine binary conditions contains 2⁹ = 512 columns. Testing all combinations is impractical. The standard mitigation is to use a **collapsed table** — one column per failing condition, plus one fully-passing column — but this means some multi-failure combinations go untested. TC-11 covers three simultaneous failures, which provides reasonable confidence, but a team requiring exhaustive coverage would need additional tooling (pairwise testing, combinatorial test design).

### 3.2 Conditions Must Be Independent
Decision tables assume each condition can vary freely regardless of what the other conditions are. If two conditions are logically coupled — for example, if a routing number could never be valid while the account number is invalid because they share a check-digit scheme — the table overstates the number of distinct cases. The e-check simulator's nine rules are structurally independent, so this limitation does not bite here, but designers should verify independence before building the table.

### 3.3 No Coverage of Ordering or Timing
Decision tables describe *what* the system does given a set of inputs. They say nothing about *when* or *in what order* things happen. If a requirement states "the routing number must be validated before the account number is displayed," that ordering constraint is invisible to decision table testing and requires a different technique (state-machine testing, integration testing).

### 3.4 No Performance or Load Coverage
A decision table test confirms functional correctness under a single submission. It does not tell you whether the system stays correct under 500 simultaneous submissions, nor whether validation completes within an acceptable latency bound. Performance testing is a separate discipline.

### 3.5 Boundary Values Require a Companion Technique
The routing-number rule requires exactly 9 digits. The decision table treats this as a binary condition: either the value is 9 digits (pass) or it is not (fail). It does not automatically generate the boundary inputs — 8 digits, 9 digits, 10 digits — that confirm the boundary is implemented correctly. TC-02 (8-digit routing number) covers the lower boundary by hand, but a systematic boundary-value analysis pass should accompany the decision table to fill that gap.

### 3.6 Condition Definitions Must Be Precise
If the requirement for "phone number" says only "must be a valid phone number," the rule is ambiguous: does a 7-digit local number pass? Does a +1 country code pass? The decision table only works well when every condition is defined precisely enough that a developer and a tester would independently write the same validator. Vague requirements surface as disagreements during table construction rather than during testing, which is actually a benefit — but the upfront precision investment is real.

---

## 4. The Sample Application

### 4.1 Technology Choice

The simulator is built in **Python 3** using **Streamlit**, a framework that turns a plain Python script into a browser-accessible web application with no separate HTML, CSS, or JavaScript required. The choice is deliberate: Python is the dominant language in data science and financial analytics, and Streamlit is widely used for internal tools in those domains. Rebuilding the simulator in Python makes the methodology accessible to practitioners who are comfortable with Python but do not work in TypeScript or React.

Streamlit's execution model suits the decision-table pattern cleanly. Rather than maintaining a reactive state graph (as React does), Streamlit **re-runs the entire script top-to-bottom every time a widget changes**. Each re-run re-evaluates all nine rules against the current field values, so the decision table is always current — no explicit event listeners, no debouncing, no `useEffect` hooks.

### 4.2 Application Structure

```
artifacts/echeck-python/
└── app.py          ← single-file application (~280 lines of Python)

.streamlit/
└── config.toml     ← server port and host configuration
```

Running the application:
```bash
streamlit run artifacts/echeck-python/app.py --server.port 5000
```

### 4.3 Screenshot — Initial State (All Rules Pending)

![E-Check Payment Simulator — initial state](Assignments/Images/Vibe_Code_2/py-app-initial.jpg)

The left panel is the payment form. The right panel is the live decision table. On first load, all nine rows show **PENDING** because no field has been touched yet. As soon as a field receives input the corresponding row resolves to **PASS** or **FAIL** without any button being clicked.

---

## 5. Key Code Snippets

### 5.1 The Decision Rules Array

All nine rules are defined as Python dictionaries in a single `RULES` list. Each entry carries a machine key, a display label, a human-readable requirement string, and a `validate` lambda that takes the raw string value and returns a boolean.

```python
RULES = [
    {
        "key":         "routing",
        "label":       "Routing Number",
        "requirement": "Exactly 9 numeric digits",
        "validate":    lambda v: bool(re.fullmatch(r"\d{9}", v.strip())),
    },
    {
        "key":         "account",
        "label":       "Account Number",
        "requirement": "8 to 12 numeric digits",
        "validate":    lambda v: bool(re.fullmatch(r"\d{8,12}", v.strip())),
    },
    {
        "key":         "phone",
        "label":       "Phone Number",
        "requirement": "Exactly 10 digits (formatting ignored)",
        "validate":    lambda v: bool(re.fullmatch(r"\d{10}", re.sub(r"\D", "", v))),
    },
    {
        "key":         "amount",
        "label":       "Payment Amount",
        "requirement": "Greater than $0.00",
        "validate":    lambda v: (
            bool(re.fullmatch(r"\d+(\.\d{1,2})?", v.strip()))
            and float(v.strip()) > 0
        ) if re.fullmatch(r"\d+(\.\d{1,2})?", v.strip()) else False,
    },
    # … five more rules for name, address, state, and ZIP
]
```

This structure keeps every rule self-contained. Adding a tenth rule means adding one dictionary to the list — the rendering loop and evaluation logic need no changes.

### 5.2 Reading Live Values and Evaluating the Table

Streamlit persists widget values in `st.session_state` between re-runs. After the form widgets are declared, the script reads the current values and runs every rule:

```python
# Read the current value of each field from session state
current = {
    "first_name": st.session_state.get("first_name", ""),
    "routing":    st.session_state.get("routing", ""),
    "account":    st.session_state.get("account", ""),
    "amount":     st.session_state.get("amount", ""),
    # … etc.
}

# Evaluate every rule — this runs on every widget interaction
evaluations = []
for rule in RULES:
    val = current.get(rule["key"], "")
    try:
        passed = rule["validate"](val)
    except Exception:
        passed = False
    evaluations.append({
        "rule":   rule,
        "passed": passed,
        "filled": len(str(val).strip()) > 0,
    })

all_pass     = all(e["passed"] for e in evaluations)
failed_rules = [e["rule"]["label"] for e in evaluations if not e["passed"]]
```

The `try/except` wrapper prevents a malformed input (for example, a stray letter in the amount field) from raising an unhandled exception — it simply counts as a `False` result for that rule.

### 5.3 Rendering the Decision Table

The table is rendered row by row. Each row's badge is determined by three pieces of state: whether the field has been filled, whether it passed validation, and whether the form has been submitted at least once.

```python
for ev in evaluations:
    rule   = ev["rule"]
    filled = ev["filled"]
    passed = ev["passed"]

    # Determine badge text and colour
    if not filled and not st.session_state.submitted:
        badge, color = "⬜ PENDING", "#888"
    elif passed:
        badge, color = "✅ PASS",    "#22863a"
    else:
        badge, color = "❌ FAIL",    "#cb2431"

    # Render one row as three Streamlit columns
    c1, c2, c3 = st.columns([2, 3, 1])
    with c1:
        st.markdown(f"**{rule['label']}**")
    with c2:
        st.markdown(f"<small>{rule['requirement']}</small>",
                    unsafe_allow_html=True)
    with c3:
        st.markdown(
            f"<span style='color:{color};font-weight:700;'>{badge}</span>",
            unsafe_allow_html=True,
        )
```

### 5.4 Submit Handler and Transaction Log

On form submission the handler checks whether every rule passed, records the verdict, and prepends a transaction record to `st.session_state.transactions` for display in the history panel below:

```python
if submitted:
    st.session_state.submitted = True

    if all_pass:
        st.session_state.verdict  = "approved"
        st.session_state.ref_code = generate_ref()     # e.g. "EC-K4R2WX9A"
    else:
        st.session_state.verdict      = "declined"
        st.session_state.failed_rules = failed_rules

    # Record the transaction in session history
    payer = f"{current['first_name'].strip()} {current['last_name'].strip()}".strip()
    st.session_state.transactions.insert(0, {
        "timestamp":    datetime.now(),
        "payer_name":   payer or "—",
        "amount":       current["amount"],
        "verdict":      st.session_state.verdict,
        "ref_code":     st.session_state.ref_code,
        "failed_rules": failed_rules if not all_pass else [],
    })
```

### 5.5 Session State — Surviving Re-Runs

Because Streamlit re-runs the whole script on every interaction, any Python variable that needs to persist across interactions must be stored in `st.session_state`. The pattern used throughout the app:

```python
# Initialise once; subsequent re-runs find the key already present
if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "verdict" not in st.session_state:
    st.session_state.verdict = None    # None | "approved" | "declined"
```

This is the Streamlit equivalent of React's `useState` — it is the primary mental-model shift Python developers must make when moving to Streamlit.

---

## 6. Sunny Day Scenario — TC-01: All Fields Valid

### Objective
Confirm that a submission where every field satisfies its rule produces an **APPROVED** verdict and a settlement reference code.

### Input Data

| Field | Value | Rule satisfied |
|-------|-------|:--------------:|
| First Name | Emad | ✓ |
| Last Name | Fattah | ✓ |
| Street Address | 1234 Holly Dr | ✓ |
| State | MI | ✓ |
| ZIP Code | 48099 | ✓ |
| Phone Number | (444) 555-6666 | ✓ |
| Routing Number | 213123123 | ✓ |
| Account Number | 73648291 | ✓ |
| Payment Amount | 20.00 | ✓ |

### Decision Table Output (command-line verification)

```
Sunny Day Scenario — TC-01: All Fields Valid
All 9 conditions are satisfied. The payment clears every underwriting check.

  Rule                 Requirement                            Status
  --------------------------------------------------------------------------
  First Name           At least 1 non-whitespace character     PASS
  Last Name            At least 1 non-whitespace character     PASS
  Street Address       At least 1 non-whitespace character     PASS
  State                Valid US state selected                 PASS
  ZIP Code             Exactly 5 numeric digits                PASS
  Phone Number         Exactly 10 digits (non-numeric chars stripped)  PASS
  Routing Number       Exactly 9 numeric digits                PASS
  Account Number       8 to 12 numeric digits                  PASS
  Payment Amount       Numeric value greater than $0.00        PASS
  --------------------------------------------------------------------------

  PAYMENT APPROVED — all checks passed; queued for settlement.
```

**Result:** ✅ APPROVED — matches expected outcome.

**What the browser shows:** All nine rows in the decision table turn green. The verdict banner displays a green "PAYMENT APPROVED" box with the generated reference code (e.g. `EC-K4R2WX9A`). A green transaction card is appended to the history panel.

**Observation:** The phone number `(444) 555-6666` contains parentheses, a space, and a hyphen. The validator strips all non-numeric characters with `re.sub(r"\D", "", v)` before checking for exactly 10 digits, so the formatted version passes identically to the bare `4445556666` form. This is the correct behaviour for real-world payment forms where users enter phone numbers in varied formats.

---

## 7. Rainy Day Scenarios

### 7.1 TC-02 — Routing Number Too Short (8 digits instead of 9)

**Objective:** Confirm that a single-field failure is sufficient to decline the payment, even when all other eight rules pass perfectly.

**What changed from TC-01:** `routing = "12312312"` (8 digits — one digit removed).

```
Rainy Day Scenario — TC-02: Routing Number Too Short

  Rule                 Requirement                            Status
  --------------------------------------------------------------------------
  First Name           At least 1 non-whitespace character     PASS
  Last Name            At least 1 non-whitespace character     PASS
  Street Address       At least 1 non-whitespace character     PASS
  State                Valid US state selected                 PASS
  ZIP Code             Exactly 5 numeric digits                PASS
  Phone Number         Exactly 10 digits (non-numeric chars stripped)  PASS
  Routing Number       Exactly 9 numeric digits                FAIL  ← 8 digits
  Account Number       8 to 12 numeric digits                  PASS
  Payment Amount       Numeric value greater than $0.00        PASS
  --------------------------------------------------------------------------

  PAYMENT DECLINED — one or more checks failed.
```

**Result:** ✅ DECLINED — matches expected outcome.

**Observation:** Eight of nine rules pass, but the conjunctive logic means there is no partial approval. One failure is conclusive. In the browser, only the Routing Number row turns red; all others remain green. The declined transaction card lists "Routing Number" as the sole failed check.

This scenario is important because it confirms the **precision boundary** of the routing-number rule: 8 digits look almost correct and would likely pass a human visual inspection. The automated validator catches it without ambiguity.

---

### 7.2 TC-11 — Multiple Fields Invalid Simultaneously

**Objective:** Confirm that when more than one field fails, all failing rules are identified and reported together — not just the first failure encountered.

**What changed from TC-01:**
- `zip_code = "48O99"` (letter O instead of digit 0)
- `account  = "7364829"` (7 digits — one below the 8-digit minimum)
- `amount   = "0.00"` (not greater than zero)

```
Rainy Day Scenario — TC-11: Multiple Fields Invalid

  Rule                 Requirement                            Status
  --------------------------------------------------------------------------
  First Name           At least 1 non-whitespace character     PASS
  Last Name            At least 1 non-whitespace character     PASS
  Street Address       At least 1 non-whitespace character     PASS
  State                Valid US state selected                 PASS
  ZIP Code             Exactly 5 numeric digits                FAIL  ← contains letter
  Phone Number         Exactly 10 digits (non-numeric chars stripped)  PASS
  Routing Number       Exactly 9 numeric digits                PASS
  Account Number       8 to 12 numeric digits                  FAIL  ← only 7 digits
  Payment Amount       Numeric value greater than $0.00        FAIL  ← zero amount
  --------------------------------------------------------------------------

  PAYMENT DECLINED — one or more checks failed.
```

**Result:** ✅ DECLINED — all three failures reported simultaneously.

**Observation:** This case tests the **report-all-failures** behaviour. A system that short-circuits on the first failure would only report ZIP Code and hide the account and amount problems. The evaluation loop iterates over all nine rules regardless of earlier results, so a payer receiving the declined notice sees the complete picture and can fix all three issues in one correction cycle rather than submitting three times.

The ZIP code failure (`48O99`) also tests a common **transcription error**: the letter O looks like the digit 0 in many fonts. The regex `\d{5}` correctly rejects the letter, whereas a human reviewer might miss it at a glance.

---

### 7.3 TC-08 — First Name Is Whitespace Only

**Objective:** Verify the edge case where a field appears to contain input (spaces are visible in the text box) but the trimmed value is effectively empty.

**What changed from TC-01:** `first_name = "   "` (three spaces).

```
Rainy Day Scenario — TC-08: First Name Is Whitespace Only

  Rule                 Requirement                            Status
  --------------------------------------------------------------------------
  First Name           At least 1 non-whitespace character     FAIL  ← trimmed to ""
  Last Name            At least 1 non-whitespace character     PASS
  Street Address       At least 1 non-whitespace character     PASS
  State                Valid US state selected                 PASS
  ZIP Code             Exactly 5 numeric digits                PASS
  Phone Number         Exactly 10 digits (non-numeric chars stripped)  PASS
  Routing Number       Exactly 9 numeric digits                PASS
  Account Number       8 to 12 numeric digits                  PASS
  Payment Amount       Numeric value greater than $0.00        PASS
  --------------------------------------------------------------------------

  PAYMENT DECLINED — one or more checks failed.
```

**Result:** ✅ DECLINED — whitespace-only name correctly rejected.

**Observation:** The Python validator uses `len(v.strip()) >= 1`. Calling `.strip()` removes leading and trailing whitespace before measuring length, so `"   "` becomes `""` which has length 0 — a clean failure. This matters because a payer might accidentally press the spacebar in a name field, leaving a field that *looks* populated. Without the trim check, a name of three spaces would silently pass and produce a settlement record with a blank payer name.

---

## 8. Conclusion

### 8.1 Problems Encountered

**Streamlit's re-run execution model requires a different mental model.**  
The biggest conceptual challenge was understanding that Streamlit does not have persistent variables in the conventional sense. Every time a user types a character or selects a dropdown option, the entire Python script runs from the top. Any state that needs to survive between interactions — the transaction history, the last verdict, whether the form has been submitted — must be stored explicitly in `st.session_state`. Developers accustomed to object-oriented or React-style frameworks tend to write `self.transactions = []` or `const [history, setHistory] = useState([])` and expect the value to persist; in Streamlit that approach silently resets on every keystroke. The fix is consistent use of the `if "key" not in st.session_state: st.session_state.key = default` pattern before any widget declaration.

**Port conflict and proxy routing.**  
Running multiple services in the same workspace (a React app at `/` and a Streamlit app on port 5000) required understanding how the Replit proxy routes traffic. Since both cannot occupy the root path simultaneously, the Streamlit app is accessed by switching the preview dropdown to the named workflow rather than visiting `/` directly. This is not a bug in either framework — it is a workspace configuration detail — but it was a non-obvious step.

**Regex safety for the amount field.**  
The amount validator must first confirm the string matches the numeric pattern before calling `float()` on it, otherwise a non-numeric string raises a `ValueError` inside the lambda. The solution was a guard expression:
```python
lambda v: (
    bool(re.fullmatch(r"\d+(\.\d{1,2})?", v.strip())) and float(v.strip()) > 0
) if re.fullmatch(r"\d+(\.\d{1,2})?", v.strip()) else False
```
This evaluates the regex twice — once to guard and once inside the conditional — which is slightly redundant. A cleaner version would extract a helper function, but the inline lambda was kept for consistency with the other rules. The outer `try/except` in the evaluation loop provides a final safety net regardless.

**Streamlit's form widget scoping.**  
Widgets declared inside `st.form(...)` only submit their values when the form's submit button is clicked — they do not trigger re-runs on every keystroke the way widgets outside a form do. This means the decision table, which needs live per-keystroke updates, cannot be placed *inside* the form. The solution is to render the form on the left and the decision table on the right in separate column contexts, reading values from `st.session_state` (which Streamlit updates for form widgets on every internal interaction) rather than from the widget return values directly.

---

### 8.2 What Was Learned About AI Tools

**AI accelerates scaffolding, not logic design.**  
The AI assistant (Replit Agent) generated the structural boilerplate — page layout, column definitions, HTML badge styling, session state initialisation — very quickly and accurately. Where it required more guidance was in the *logic design*: deciding which edge cases to test (whitespace-only names, letter-O in a ZIP code), choosing which scenarios best illustrated the methodology, and writing the analytical prose. The division of labour that worked well was: human sets the test objectives and scenario rationale, AI implements the code and document structure.

**Prompt precision determines output quality.**  
Requests like "add a decision table" produced reasonable but generic results. Requests like "add a live decision table that shows PENDING for untouched fields, PASS when valid, and FAIL when invalid, updating on every keystroke without a form submit" produced exactly the right behaviour on the first attempt. The lesson is that investing thirty seconds in a precise specification saves several rounds of correction.

**AI tools handle framework migration well.**  
Translating the TypeScript/React implementation to Python/Streamlit was handled without significant errors. The AI correctly mapped React concepts to Streamlit equivalents: `useState` → `st.session_state`, `useMemo` → simple re-evaluation on each script run, `watch()` → `st.session_state.get()`. Where the frameworks differ significantly (the form-submission model, the re-run architecture), the translation required a brief explanation rather than a simple one-to-one substitution — but the AI absorbed those corrections quickly and applied them consistently.

**AI-generated code benefits from human test review.**  
The initial amount validator did not include the guard against non-numeric strings, meaning it would raise an exception on inputs like `"abc"`. This was caught by writing the rainy-day scenarios and observing the error in the console. AI tools tend to generate the happy path reliably and to miss defensive edge cases — which is exactly where human review and structured test design add the most value. Decision table methodology is, in this sense, a productive complement to AI-assisted development: the AI builds fast, the decision table ensures systematic coverage of the conditions the AI might overlook.

**The combination of AI + structured methodology is genuinely productive.**  
For a project of this scope — a validated payment form with a live decision table, a transaction history, and a comprehensive test report — the AI handled approximately 80% of the implementation work. The remaining 20% was analytical: choosing the right methodology, identifying edge cases, writing scenario rationale, and reviewing the generated code for correctness. The result is a more complete and more thoroughly documented project than either approach alone would have produced in the same time.

---

*End of report.*
