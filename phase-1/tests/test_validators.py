"""Tests for input validation functions.

Test cases cover all validators:
- validate_title
- validate_description
- validate_task_id
- validate_menu_choice
- validate_confirmation
"""

from validators.input_validators import (
    validate_title,
    validate_description,
    validate_task_id,
    validate_menu_choice,
    validate_confirmation,
)


# validate_title tests
def test_validate_title_valid():
    """Test valid title."""
    is_valid, msg, title = validate_title("Buy groceries")
    assert is_valid is True
    assert msg == ""
    assert title == "Buy groceries"


def test_validate_title_with_whitespace():
    """Test title with leading/trailing whitespace."""
    is_valid, msg, title = validate_title("  Buy groceries  ")
    assert is_valid is True
    assert title == "Buy groceries"


def test_validate_title_empty():
    """Test empty title."""
    is_valid, msg, title = validate_title("")
    assert is_valid is False
    assert "cannot be empty" in msg.lower()
    assert title == ""


def test_validate_title_whitespace_only():
    """Test title with only whitespace."""
    is_valid, msg, title = validate_title("   ")
    assert is_valid is False
    assert "cannot be empty" in msg.lower()


def test_validate_title_too_long():
    """Test title exceeding 200 characters."""
    long_title = "a" * 201
    is_valid, msg, title = validate_title(long_title)
    assert is_valid is False
    assert "too long" in msg.lower()
    assert "200" in msg


def test_validate_title_max_length():
    """Test title at exactly 200 characters."""
    max_title = "a" * 200
    is_valid, msg, title = validate_title(max_title)
    assert is_valid is True
    assert title == max_title


# validate_description tests
def test_validate_description_valid():
    """Test valid description."""
    is_valid, msg, desc = validate_description("Task description")
    assert is_valid is True
    assert msg == ""
    assert desc == "Task description"


def test_validate_description_empty():
    """Test empty description (valid)."""
    is_valid, msg, desc = validate_description("")
    assert is_valid is True
    assert desc == ""


def test_validate_description_whitespace():
    """Test description with whitespace."""
    is_valid, msg, desc = validate_description("  Description  ")
    assert is_valid is True
    assert desc == "Description"


def test_validate_description_too_long():
    """Test description exceeding 1000 characters."""
    long_desc = "a" * 1001
    is_valid, msg, desc = validate_description(long_desc)
    assert is_valid is False
    assert "too long" in msg.lower()
    assert "1000" in msg


def test_validate_description_max_length():
    """Test description at exactly 1000 characters."""
    max_desc = "a" * 1000
    is_valid, msg, desc = validate_description(max_desc)
    assert is_valid is True
    assert desc == max_desc


# validate_task_id tests
def test_validate_task_id_valid():
    """Test valid task ID."""
    is_valid, msg, task_id = validate_task_id("1")
    assert is_valid is True
    assert msg == ""
    assert task_id == 1


def test_validate_task_id_with_whitespace():
    """Test task ID with whitespace."""
    is_valid, msg, task_id = validate_task_id("  42  ")
    assert is_valid is True
    assert task_id == 42


def test_validate_task_id_non_numeric():
    """Test non-numeric task ID."""
    is_valid, msg, task_id = validate_task_id("abc")
    assert is_valid is False
    assert "numeric" in msg.lower()
    assert task_id is None


def test_validate_task_id_zero():
    """Test zero task ID (invalid)."""
    is_valid, msg, task_id = validate_task_id("0")
    assert is_valid is False
    assert task_id is None


def test_validate_task_id_negative():
    """Test negative task ID (invalid)."""
    is_valid, msg, task_id = validate_task_id("-5")
    assert is_valid is False
    assert task_id is None


def test_validate_task_id_float():
    """Test float task ID (invalid)."""
    is_valid, msg, task_id = validate_task_id("1.5")
    assert is_valid is False
    assert task_id is None


# validate_menu_choice tests
def test_validate_menu_choice_valid():
    """Test valid menu choices (1-6)."""
    for choice in ["1", "2", "3", "4", "5", "6"]:
        is_valid, msg, val = validate_menu_choice(choice)
        assert is_valid is True
        assert msg == ""
        assert val == int(choice)


def test_validate_menu_choice_with_whitespace():
    """Test menu choice with whitespace."""
    is_valid, msg, choice = validate_menu_choice("  3  ")
    assert is_valid is True
    assert choice == 3


def test_validate_menu_choice_out_of_range_low():
    """Test menu choice below 1."""
    is_valid, msg, choice = validate_menu_choice("0")
    assert is_valid is False
    assert "1-6" in msg


def test_validate_menu_choice_out_of_range_high():
    """Test menu choice above 6."""
    is_valid, msg, choice = validate_menu_choice("7")
    assert is_valid is False
    assert "1-6" in msg


def test_validate_menu_choice_non_numeric():
    """Test non-numeric menu choice."""
    is_valid, msg, choice = validate_menu_choice("abc")
    assert is_valid is False
    assert "1-6" in msg


# validate_confirmation tests
def test_validate_confirmation_yes_variations():
    """Test 'yes' variations."""
    for val in ["y", "Y", "yes", "YES", "Yes", "  y  ", "  YES  "]:
        is_valid, msg, confirmed = validate_confirmation(val)
        assert is_valid is True
        assert msg == ""
        assert confirmed is True


def test_validate_confirmation_no_variations():
    """Test 'no' variations."""
    for val in ["n", "N", "no", "NO", "No", "  n  ", "  NO  "]:
        is_valid, msg, confirmed = validate_confirmation(val)
        assert is_valid is True
        assert msg == ""
        assert confirmed is False


def test_validate_confirmation_invalid():
    """Test invalid confirmation input."""
    for val in ["maybe", "yep", "nope", "1", ""]:
        is_valid, msg, confirmed = validate_confirmation(val)
        assert is_valid is False
        assert "y" in msg.lower() and "n" in msg.lower()


if __name__ == "__main__":
    # Title tests
    test_validate_title_valid()
    test_validate_title_with_whitespace()
    test_validate_title_empty()
    test_validate_title_whitespace_only()
    test_validate_title_too_long()
    test_validate_title_max_length()

    # Description tests
    test_validate_description_valid()
    test_validate_description_empty()
    test_validate_description_whitespace()
    test_validate_description_too_long()
    test_validate_description_max_length()

    # Task ID tests
    test_validate_task_id_valid()
    test_validate_task_id_with_whitespace()
    test_validate_task_id_non_numeric()
    test_validate_task_id_zero()
    test_validate_task_id_negative()
    test_validate_task_id_float()

    # Menu choice tests
    test_validate_menu_choice_valid()
    test_validate_menu_choice_with_whitespace()
    test_validate_menu_choice_out_of_range_low()
    test_validate_menu_choice_out_of_range_high()
    test_validate_menu_choice_non_numeric()

    # Confirmation tests
    test_validate_confirmation_yes_variations()
    test_validate_confirmation_no_variations()
    test_validate_confirmation_invalid()

    print("All validator tests passed!")
