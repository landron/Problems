/*
https://leetcode.com/problems/valid-parentheses/
*/
package problems

/*
s consists of parentheses only '()[]{}'.
*/
func AreParanthesesValid(s string) bool {
	if len(s) < 1 || len(s) > 10_000 {
		panic("constraint violation: length must be between 1 and 10^4")
	}

	stack := make([]rune, 0, len(s))
	for _, ch := range s {
		switch ch {
		case '(', '{', '[':
			stack = append(stack, ch)
		case ')', '}', ']':
			if len(stack) == 0 || !isMatch(stack[len(stack)-1], ch) {
				return false
			}
			stack = stack[:len(stack)-1]
		}
	}

	return len(stack) == 0
}

func isMatch(a, b rune) bool {
	switch b {
	case ')':
		return a == '('
	case '}':
		return a == '{'
	case ']':
		return a == '['
	default:
		return false
	}
}
