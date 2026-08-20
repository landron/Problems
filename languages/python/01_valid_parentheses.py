def is_valid(s: str) -> bool:
    assert s and len(s) <= 10**4, "constraint violation"

    stack = []
    for ch in s:
        if ch in "({[":
            stack.append(ch)
        elif ch in ")}]":
            if not stack:
                return False
            if ch == ")" and stack[-1] != "(":
                return False
            if ch == "]" and stack[-1] != "[":
                return False
            if ch == "}" and stack[-1] != "{":
                return False
            stack.pop()

    return not stack
