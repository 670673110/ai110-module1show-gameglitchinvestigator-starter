# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**


Answer: I used Claude Code in VS Code for a series of tasks:
        - Explain why the hints were backwards.
        - Fix the hint logic.
        - Fix the attempts count.
        - Write tests in `tests/test_game_logic.py` for these two fixes.

**What did the agent do?**

Answer: -Read `app.py` and found two causes for the bad hints. First, the "Go HIGHER" and "Go LOWER" messages were swapped in `check_guess`. Second, on every even attempt the secret was turned into a string, so the guess was compared as text (for example, `"9" > "50"` is True).
        - Edited `app.py` to swap the messages back and always pass the secret as an int. This also removed the `try/except TypeError` branch.
        - Found that `attempts` started at `1` on first load but at `0` after New Game, so the first game gave one fewer attempt than allowed. Changed the starting value to `0`.
        - Found that "Attempts left" was drawn before the guess was processed, so it showed the old number. Put it in an `st.empty()` placeholder with a `show_attempts_left()` helper and redrew it after each guess.
        - Moved `check_guess` from `app.py` into `logic_utils.py` and made `app.py` import it, because the tests import from `logic_utils`.
        - Wrote 9 new tests and updated the 3 existing ones. The attempts tests use Streamlit's `AppTest` to run the real app.
        - Ran `pytest` (12 passed). It then put the old bugs back in a scratch copy of the project and ran the tests again. 8 tests failed, which shows the tests actually catch the bugs.

**What did you have to verify or fix manually?**

Answer: - The agent first tried `venv/`, which doesn't have Streamlit installed, and had to switch to `.venv/`. Tests must be run with `.venv/bin/python -m pytest tests`.
        - When `check_guess` moved to `logic_utils.py`, the `#Logic breaks here:` comment I had added was deleted, so I had to check where it went.
        - The agent changed the 3 starter tests. They expected `check_guess` to return only a string, but the app needs `(outcome, message)`. I reviewed this change to make sure it was correct.
        - The agent noticed bugs it did not fix: New Game doesn't reset status, history, or score; invalid input still uses up an attempt; and the win score is off by one (`attempt_number + 1`). I decided which of these to work on myself.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Numbers that compare differently as text (9 vs 50, 100 vs 50) | Same prompt | `test_hint_compares_numbers_not_strings` | Yes | As strings, `"9" > "50"` and `"100" < "50"`. This checks we compare numbers, not text. |
| Guesses right next to the secret (49 and 51) | Same prompt | `test_off_by_one_guesses` | Yes | Boundary values are where comparison mistakes usually show up. |
| Hint on an even-numbered attempt | Same prompt | `test_hint_correct_on_even_attempts` (runs the app with `AppTest`) | Yes | The old code only broke on even attempts, so a test of the first guess alone would miss it. |
| Attempt count on a new session | Same prompt | `test_new_session_starts_with_zero_attempts` | Yes | The count used to start at 1, so the player lost one attempt. |
| "Attempts left" right after a guess | Same prompt | `test_attempts_left_updates_right_after_guess` | Yes | The display used to show the old number until the next rerun. |
| Using all attempts (Normal = 8) | Same prompt | `test_player_gets_full_attempt_limit` | Yes | Checks the game is still playing after 7 wrong guesses and ends after the 8th. |
| New Game resets the count | Same prompt | `test_new_game_resets_attempts` | Yes | The count should go back to 0 and show 8 attempts left. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```
answer: explain why hint were backward
        fix the hint logic
        the attempts not count correct, why
        fix the attempts part

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
