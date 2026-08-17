# Vibe_Coding Assignment #3

**State Transition Testing / Control Flow Testing / Data Flow Testing**

**Student:** Emad Fattah

**Class:** MSSE640

**Instructor:** Randell Grainer

---
# ATM Transaction Runner — Software Testing Project Report

[ATM Project Link](https://verbose-memory-4q747v7jvgr4f4jw.github.dev) . For more info about the link see [Running The Python Script](#running_python_script) section.



**Project:** ATM State Machine with State Transition, Control Flow, and Data Flow Testing

**Language:** Python 3 (standard library `unittest`)

**Test results:** 44 / 44 tests passed

---

## Table of Contents

A. Introduction

B. Vibe Coding Assignment

C. Conclusion

___

## A. Introduction

### The Fundamentals of the Three Testing Techniques

#### 1. State Transition Testing

State transition testing treats the system as a **finite state machine**: at any moment the system is in exactly one state, and events move it from one state to another along defined transitions. Test cases are designed to cover:

- **Every valid transition** (each arrow in the state diagram is exercised at least once), and
- **Every invalid transition** (events fired in the wrong state must be rejected safely, not crash the system).

The ATM in this project has four states:

| State | Meaning |
|---|---|
| `IDLE` | No card in the machine |
| `AWAITING_PIN` | Card accepted, waiting for the PIN |
| `AUTHENTICATED` | Correct PIN entered; transactions allowed |
| `CARD_BLOCKED` | Three wrong PINs — card is confiscated logically |

The transitions tested were:

```
IDLE ──insert valid card──────► AWAITING_PIN
IDLE ──insert blocked card────► CARD_BLOCKED
AWAITING_PIN ──correct PIN────► AUTHENTICATED
AWAITING_PIN ──3 wrong PINs───► CARD_BLOCKED
AUTHENTICATED ──eject card────► IDLE
CARD_BLOCKED ──eject card─────► IDLE
```

Invalid transitions — such as entering a PIN while the machine is `IDLE`, inserting a second card while one is already inside, or withdrawing before authentication — are tested to confirm the machine raises a controlled error (`RuntimeError`) and stays in a consistent state. **12 state-transition tests** cover these paths.

#### 2. Control Flow Testing

Control flow testing is a **white-box** technique: it looks at the branches inside the code (`if`/`else` decisions, loops, guards) and designs tests so that **every branch is executed at least once** in both its true and false directions. The goal is branch coverage — no decision in the code should go untested.

The ATM's `withdraw()` method is the richest control-flow target, since it contains a chain of guards:

1. Machine must be `AUTHENTICATED`
2. Amount must be a valid number (not text, not `None`)
3. Amount must be positive (not zero, not negative, not NaN)
4. Amount must not exceed the $10,000 single-transaction limit
5. The ATM must not be out of cash
6. The ATM must hold at least the requested amount
7. The account balance must cover the amount

**15 control-flow tests** force every one of these guards to fire (rainy day) and also pass through them all successfully (sunny day). The `enter_pin()` branches — correct PIN / wrong PIN with attempts remaining / third wrong PIN causing a block — are each covered as well.

#### 3. Data Flow Testing

Data flow testing follows **variables** rather than branches. Every variable has a lifecycle:

- **Definition (def):** the variable receives a value
- **Use:** the value is read in a computation or condition
- **Kill:** the value is overwritten or destroyed

Tests trace def→use→kill paths to catch bugs like using a variable before it is defined, or a failed operation accidentally corrupting a value. The variables traced in this project:

| Variable | Defined | Used | Killed |
|---|---|---|---|
| `account.balance` | At account creation | Read by `check_balance()`, checked before withdrawal | Overwritten by a successful withdrawal |
| `atm_cash` | At ATM initialization | Checked before dispensing | Reduced by each successful withdrawal |
| `last_receipt` | `None` initially; defined by first successful withdrawal | Read after a withdrawal | Re-defined (old value killed) by the next withdrawal |
| `pin_attempts` | Reset to 0 on card insert | Compared to the 3-attempt limit | Reset to 0 on correct PIN |

**17 data-flow tests** verify, critically, that **failed operations do not mutate data**: a rejected withdrawal must leave the balance, the ATM cash, and the last receipt exactly as they were.

### How the ATM Was Built Around These Fundamentals

The ATM was deliberately designed *to be testable* by all three techniques:

- The state machine is explicit — a single `state` field with named constants — so every transition testable by state transition testing is visible and enforced in code.
- Every business rule is a separate, ordered guard clause, giving control flow testing one clean branch per rule.
- Key data (balance, ATM cash, PIN attempts, receipt) is only mutated at a single, well-defined point *after all guards pass*, which makes the def→use→kill paths of data flow testing easy to trace and verify.
- All inputs are validated at the entry point of each method, so bad data (empty strings, `None`, negative numbers) produces a clear error instead of a crash mid-transaction.

---

## B. Vibe Coding Assignment

### Why Python

Python was the natural choice for this project for several reasons:

1. **Built-in testing framework.** The `unittest` module ships with Python — no installation, no configuration. The entire project (domain model + 44 tests) is a single self-contained file that runs with one command: `python atm_testing_demo.py`.
2. **Readability.** Python's clean syntax makes the state machine and the guard clauses read almost like the specification itself, which is ideal when the code is the subject being studied.
3. **Rapid iteration.** Ideas could be tested instantly in a Jupyter notebook — including an interactive mode where the ATM asks the user to insert a card, enter a PIN, and choose a withdrawal amount using `input()`.
4. **Dynamic typing as a testing opportunity.** Because Python will happily pass a string or `None` where a number is expected, the code *must* defend itself — which produced excellent rainy-day test cases (e.g., `withdraw("abc")`, `enter_pin(None)`).

### Sunny Day Scenarios (Happy Path)

Sunny-day tests verify the system does the right thing when everything goes well:

| # | Scenario | Expected result |
|---|---|---|
| 1 | Insert card `1111` (Emad Fattah) | Machine moves to `AWAITING_PIN` |
| 2 | Enter correct PIN `1234` | Machine moves to `AUTHENTICATED`, greets the holder |
| 3 | Check balance | Returns $2,500.00 |
| 4 | Withdraw $400 | Cash dispensed, balance becomes $2,100, ATM cash drops by $400, receipt generated with date, time, masked card number, holder name, amount, and new balance |
| 5 | Eject card | Machine returns to `IDLE`; a new card can be inserted |
| 6 | One or two wrong PINs, then the correct one | Attempts counter increments, then resets to 0 on success — no block |
| 7 | Multiple sequential withdrawals | Deductions accumulate correctly on both the account and the ATM |

### Rainy Day Scenarios (Error Paths)

Rainy-day tests verify the system fails **safely and informatively**:

| # | Scenario | Expected result |
|---|---|---|
| 1 | Insert an unknown card (`9999`) | "Card not recognised" — machine stays `IDLE` |
| 2 | Three consecutive wrong PINs | Card permanently blocked; state = `CARD_BLOCKED` |
| 3 | Insert an already-blocked card | Goes straight to `CARD_BLOCKED` |
| 4 | Enter a PIN while machine is `IDLE` | Controlled `RuntimeError` — no crash |
| 5 | Withdraw text (`"abc"`) or `None` | "Invalid amount" message — no crash |
| 6 | Withdraw a negative amount or zero | Rejected by the positive-amount guard |
| 7 | Withdraw more than $10,000 | Rejected by the single-transaction limit |
| 8 | Withdraw more than the ATM holds | "ATM only has $X available" |
| 9 | ATM completely out of cash | "ATM is out of cash" |
| 10 | Withdraw more than the account balance | "Insufficient funds" |
| 11 | Failed withdrawal | Balance, ATM cash, and last receipt all remain **unchanged** |
| 12 | Create an account with a negative balance | Rejected at construction with `ValueError` |

### Test Data

| Card number | PIN | Holder | Balance |
|---|---|---|---|
| 1111 | 1234 | Emad Fattah | $2,500.00 |
| 2222 | 5678 | Bob Martinez | $840.50 |
| 3333 | 9999 | Carol Chen | $12,750.00 |
| 4444 | 0000 | David Kim | $50.00 |

ATM initial cash: $10,000 · Maximum PIN attempts: 3 · Single-transaction limit: $10,000

**Final result: all 44 tests pass (12 state transition + 15 control flow + 17 data flow).**

---

## C. Conclusion


### What Problems Did We Have?

1. **Confusing names with card numbers.** When running the ATM interactively, the card was inserted using the holder's *name* ("Alice Johnson") when the machine actually expected the *card number* ("1111"). The machine kept answering "Cannot enter PIN, machine is IDLE" — because the card insert had silently failed and the machine never left `IDLE`. The lesson: read the *first* error in a chain, not the last one; the PIN error was only a symptom.
2. **Receipt formatting vs. test assertions.** One test originally checked for the exact string `"$50.00"` in the receipt, but the receipt right-pads amounts (`$     50.00`) for alignment. The test failed even though the behavior was correct. The assertion was loosened to check for `"50.00"` — a reminder that tests should assert on *meaning*, not incidental formatting.
3. **Running tests inside Jupyter.** `unittest.main()` does not work cleanly inside a notebook (it tries to parse Jupyter's own command-line arguments). The fix was to build the test suite manually with `TestLoader` and run it with `TextTestRunner`.
4. **Interactive input pitfalls.** `input()` returns text with possible stray spaces, so `.strip()` was needed, and withdrawal amounts had to be converted with `float()` — small details that only surface when a human, not a test, drives the program.

### What Did We Learn About AI Tools?

1. **AI is fast at scaffolding, but the human must verify.** The AI produced a complete, working state machine and 44 tests quickly — but the human running the program caught the name-vs-card-number confusion that a passing test suite never revealed. Green tests do not guarantee the *documentation and instructions* are right.
2. **Precise prompts matter.** Vague requests ("it doesn't work") produced generic advice; specific ones ("it shows *Cannot enter PIN, machine is IDLE*") let the AI pinpoint the real cause immediately. The quality of the answer tracks the quality of the question.
3. **AI is an excellent explainer.** Beyond writing code, the AI translated the formal testing theory (def-use-kill chains, branch coverage, state diagrams) into runnable, commented examples — turning abstract textbook concepts into something that could be executed and observed.
4. **Iterative collaboration works best.** The project grew through small back-and-forth steps — build, run, hit a problem, fix, personalize (renaming a card holder), extend (interactive mode). AI-assisted "vibe coding" is not one big generation; it is a conversation where each round refines the result.
5. **Trust but verify data flow.** When the AI changed the account name, it had to be changed in *two* places (the Python demo and the web app's server) — a reminder that AI, like a human, must track everywhere a piece of data lives.

### Final Word

Building the ATM around the three testing techniques  rather than bolting tests on afterward  produced code that is easier to reason about, fails safely on every rainy-day path, and proves its own correctness with a single command. The combination of a readable language (Python), a systematic testing discipline, and an AI partner for scaffolding and debugging made the whole cycle  design, build, break, fix, verify  remarkably fast.

### Running The Python Script<a name="running_python_script></a>
1. To run the Code Click the link under 
   [ATM Project Link](https://verbose-memory-4q747v7jvgr4f4jw.github.dev)

2. You see the platform hereunder
   
   ![open_Link](/Assignments/Images/Vibe_Code_3/1.Openthelink.png)
   
3. Scroll down until you see the test results 44/44 tests passed
   ![scroll_down](/Assignments/Images/Vibe_Code_3/2.scrolldown_see44.png)

4. Click Run All, the system will ask you to put the card number, use (1111) or any card number in Data Test table.

![click_run](/Assignments/Images/Vibe_Code_3/3.clickrunall.png)

5. After you input the card number, put the PIN number (1234) that belongs to the card, the system will show the name and balance.

![Put_PIN](/Assignments/Images/Vibe_Code_3/3.entiercard.png)

6. After you see the name and balance you can input the amount of money to draw (for Example 1500$)

![drow_money](/Assignments/Images/Vibe_Code_3/6.Pinaccepted.png)

7. After you input the amount, the system will show you final message with remaining balance and eject the card.

![completion](/Assignments/Images/Vibe_Code_3/7.drown1500.png)

### Examples of Rainy Day Seniors 

1. Input the wrong PIN number three times.

![input_wrongPIN](/Assignments/Images/Vibe_Code_3/8.exmp3atmwrong.png)

2. Withdraw more than 10,000$

![draw1000](/Assignments/Images/Vibe_Code_3/9.Drown10.png)

3. Input letters in card number request.

![input_letters](/Assignments/Images/Vibe_Code_3/10.inputlettercardno.png)

4. Withdraw with negative amount

![neg_amount](/Assignments/Images/Vibe_Code_3/11.drown_neg.png)

___

End of Assignment 





   
      
