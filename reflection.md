# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- It always asks me to go higher even when I entered 99. It then asked me to go lower after I entered 100. I tried a few float numbers between 99 and 100, and I guess the answer is infinitely close to 100, like 99.9999. 

- When chances are used up, clicking new game doesn't work. It doesn't allow me to submit new guesses, although I can see there is an updated secret number everytime I hit the new game button. 

- It asks me to go higher even if I entered 299, which is larger than the accepted range (1 to 100). Whereas the secret number is 25, and the hint obviously doesn't match the secret number / isn't doing the comparison properly. 

---

## 2. How did you use AI as a teammate?

- I used Claude Code as my AI teammate. 
- AI diagnosis: *Has multiple intentional bugs (glitches to investigate): wrong hint directions, type confusion on even attempts, scoring rewards wrong guesses, hardcoded range in UI, new game ignores difficulty*


**Bugs fixed:**
1. Imports functions from logic_utils instead of redefining them
2. Hint messages were backwards — "Too High" said "Go HIGHER!" (should be "Go LOWER!") and vice versa
3. Type confusion bug — even-numbered attempts converted the secret to a string, breaking int comparison
4. Info message — hardcoded "between 1 and 100" now shows the actual difficulty range
5. New game — was always using randint(1, 100), now uses the selected difficulty range
6. Attempts counter — initial state changed from 1 to 0 to be consistent with new game reset

---

## 3. Debugging and testing your fixes

To decide whether a bug was really fixed, manual or AI-generated tests should be conducted for verification

```
def test_check_guess_returns_string_not_tuple():
    # Bug: check_guess returned a (outcome, message) tuple instead of just outcome string.
    # Tests would silently pass when comparing tuple == "Win" (they wouldn't, but the
    # real risk was app code unpacking incorrectly or hints being wrong.
    result = check_guess(50, 50)
    assert isinstance(result, str), "check_guess must return a string, not a tuple"


def test_hard_difficulty_range_wider_than_normal():
    # Bug: Hard difficulty returned (1, 50), making it *easier* than Normal (1, 100).
    # Hard should have a wider range than Normal to be actually harder.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard difficulty must have a wider range than Normal"


def test_update_score_too_high_always_decreases():
    # Bug: update_score gave +5 points for "Too High" on even attempt numbers,
    # rewarding wrong guesses. It should always decrease the score.
    score_before = 100
    score_after_odd = update_score(score_before, "Too High", attempt_number=1)
    score_after_even = update_score(score_before, "Too High", attempt_number=2)
    assert score_after_odd < score_before, "Score must decrease on odd attempts for Too High"
    assert score_after_even < score_before, "Score must decrease on even attempts for Too High"


def test_update_score_too_low_always_decreases():
    # Companion to the above: "Too Low" should also always decrease score.
    score_before = 100
    score_after = update_score(score_before, "Too Low", attempt_number=2)
    assert score_after < score_before, "Score must decrease for Too Low"
```

---

## 4. What did you learn about Streamlit and state?

The secret number itself doesn't change. It's because of the type confusion bug in the original  `check_guess` function of `app.py`:
```
# Original app.py — inside the submit block
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)   # even attempts: secret becomes a string
else:
    secret = st.session_state.secret        # odd attempts: secret is an int
```
On every attempt, the number of attempt is switching back and forth between an integer type and a string type, which have different comparison logic. 
---

## 5. Looking ahead: your developer habits

Go through all code files roughly before asking AI for information and solution. This makes sure that I have enough context needed to eventually solve the problem by myself if AI is not working well. 
