from pathlib import Path

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Hint direction ---

def test_too_high_tells_player_to_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_tells_player_to_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_hint_compares_numbers_not_strings():
    # As strings, "9" > "50" and "100" < "50"; numerically it's the opposite
    assert check_guess(9, 50) == ("Too Low", "📈 Go HIGHER!")
    assert check_guess(100, 50) == ("Too High", "📉 Go LOWER!")

def test_off_by_one_guesses():
    assert check_guess(51, 50)[0] == "Too High"
    assert check_guess(49, 50)[0] == "Too Low"


# --- Attempt counting (runs the Streamlit app) ---

def start_app(secret=50):
    at = AppTest.from_file(APP_PATH)
    at.session_state["secret"] = secret
    at.run()
    return at

def submit_guess(at, guess):
    at.text_input[0].input(str(guess))
    at.button[0].click()  # "Submit Guess"
    at.run()

def attempts_left_text(at):
    return at.info[0].value


def test_new_session_starts_with_zero_attempts():
    at = start_app()
    assert at.session_state["attempts"] == 0
    assert "Attempts left: 8" in attempts_left_text(at)  # Normal = 8

def test_attempts_left_updates_right_after_guess():
    at = start_app()
    submit_guess(at, 10)
    assert at.session_state["attempts"] == 1
    assert "Attempts left: 7" in attempts_left_text(at)

def test_player_gets_full_attempt_limit():
    at = start_app()
    for _ in range(7):
        submit_guess(at, 10)
    assert at.session_state["status"] == "playing"
    assert "Attempts left: 1" in attempts_left_text(at)

    submit_guess(at, 10)
    assert at.session_state["status"] == "lost"
    assert "Attempts left: 0" in attempts_left_text(at)

def test_hint_correct_on_even_attempts():
    # Even attempts used to compare as strings, which flipped this hint
    at = start_app(secret=50)
    submit_guess(at, 10)
    submit_guess(at, 9)
    assert at.session_state["attempts"] == 2
    assert "HIGHER" in at.warning[0].value

def test_new_game_resets_attempts():
    at = start_app()
    submit_guess(at, 10)
    at.button[1].click()  # "New Game"
    at.run()
    assert at.session_state["attempts"] == 0
    assert "Attempts left: 8" in attempts_left_text(at)
