package problems_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	problems "github.com/landron/problems/languages/go"
)

func TestIsValid(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{"Example 1", "()", true},
		{"Example 2", "()[]{}", true},
		{"Example 3", "(]", false},
		{"Example 4", "([])", true},
		{"Example 5", "([)]", false},
		{"Example 6", "[", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := problems.AreParanthesesValid(tt.input); got != tt.expected {
				assert.Equal(t, tt.expected, problems.AreParanthesesValid(tt.input))
			}
		})
	}
}
