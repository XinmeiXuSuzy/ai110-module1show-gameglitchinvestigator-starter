from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Bug regression tests ---

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
