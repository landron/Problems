import importlib
import pytest

is_valid = importlib.import_module("01_valid_parentheses").is_valid


def test_is_valid_direct():
    assert is_valid("()")
    assert is_valid("()[]{}")
    assert not is_valid("(]")
    assert is_valid("([])")
    assert not is_valid("([)]")
    assert not is_valid("[")


@pytest.mark.parametrize(
    "s, expected",
    [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([])", True),
        ("([)]", False),
        ("[", False),
    ],
)
def test_is_valid_parametrized(s: str, expected: bool):
    assert is_valid(s) == expected


def test_is_valid_constraints():
    with pytest.raises(AssertionError, match="constraint violation"):
        is_valid("")
