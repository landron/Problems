/*
go test -c ./Ch10_Dynamic_Programming_Fundamentals
go test -run ^TestCanonical$
*/
package dynamic_programming_test

import (
	"testing"

	"github.com/stretchr/testify/require"

	dp "problems/Ch10_Dynamic_Programming_Fundamentals"
)

func TestEditCost(t *testing.T) {
	tests := []struct {
		name   string
		source string
		target string
		want   int
	}{
		{
			name:   "identical strings",
			source: "hello",
			target: "hello",
			want:   0,
		},
		{
			name:   "empty source (pure insertions)",
			source: "",
			target: "abc",
			want:   3,
		},
		{
			name:   "empty target (pure deletions)",
			source: "abc",
			target: "",
			want:   3,
		},
		{
			name:   "single substitution 1",
			source: "cat",
			target: "cot",
			want:   1,
		},
		{
			name:   "single substitution 2",
			source: "0",
			target: "5",
			want:   1,
		},
		{
			name:   "mixed operations",
			source: "kitten",
			target: "sitting",
			want:   3, // k->s, e->i, +g
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			require.Equal(t, tt.want, dp.EditCostTopDown(tt.source, tt.target),
				"EditCostTopDown(%q, %q)", tt.source, tt.target)
			require.Equal(t, tt.want, dp.EditCostBottomUp(tt.source, tt.target),
				"EditCostBottomUp(%q, %q)", tt.source, tt.target)
		})
	}
}

func TestEditCostCanonical(t *testing.T) {
	tests := []struct {
		name   string
		source string
		target string
		want   int
	}{
		{
			name:   "canonical prefix",
			source: "hello",
			target: "hello-modified",
			want:   9,
		},
		// dpple -> daple -> datle -> date
		{
			name:   "canonical apple - date",
			source: "apple",
			target: "date",
			want:   4,
		},
		{
			name:   "canonical cherry - date",
			source: "cherry",
			target: "date",
			want:   6,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			require.Equal(t, tt.want, dp.EditCostTopDown(tt.source, tt.target),
				"EditCostTopDown(%q, %q)", tt.source, tt.target)
			require.Equal(t, tt.want, dp.EditCostBottomUp(tt.source, tt.target),
				"EditCostBottomUp(%q, %q)", tt.source, tt.target)
		})
	}
}

func TestCanonical(t *testing.T) {
	tests := []struct {
		name       string
		A          []string
		B          []string
		insertCost int32
		deleteCost int32
		expected   int64
	}{
		{
			name:       "Canonical Sample 1",
			A:          []string{"a"},
			B:          []string{"b"},
			insertCost: 10,
			deleteCost: 10,
			expected:   1,
		},
		{
			name:       "Canonical Sample 2",
			A:          []string{"line1", "line2"},
			B:          []string{"line1-modified", "line2"},
			insertCost: 5,
			deleteCost: 3,
			expected:   8,
		},
		{
			name:       "Canonical Sample 3",
			A:          []string{"apple", "cherry"},
			B:          []string{"date"},
			insertCost: 5,
			deleteCost: 3,
			expected:   7,
		},
		// delete apple, cherry -> date
		{
			name:       "Canonical Sample 3",
			A:          []string{"apple", "banana", "cherry"},
			B:          []string{"banana", "date"},
			insertCost: 5,
			deleteCost: 3,
			expected:   9,
		},
		{
			name:       "Canonical Sample 4",
			A:          []string{},
			B:          []string{},
			insertCost: 5,
			deleteCost: 3,
			expected:   0,
		},
		{
			name:       "Canonical Sample 5",
			A:          []string{},
			B:          []string{"a", "b"},
			insertCost: 2,
			deleteCost: 5,
			expected:   4,
		},
		{
			name:       "Canonical Sample 6",
			A:          []string{"a", "b"},
			B:          []string{},
			insertCost: 3,
			deleteCost: 1,
			expected:   2,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			require.Equal(t, tt.expected, dp.MinTransformationCost(tt.A, tt.B, tt.insertCost, tt.deleteCost))
		})
	}
}

func TestMinTransformationCost(t *testing.T) {
	tests := []struct {
		name       string
		A          []string
		B          []string
		insertCost int32
		deleteCost int32
		expected   int64
	}{
		{
			name:       "Sample Input 0",
			A:          []string{"0", "0"},
			B:          []string{"5", "3"},
			insertCost: 1, // Assumed baseline costs for the sample
			deleteCost: 1,
			expected:   2,
		},
		{
			name:       "Sample Input 1",
			A:          []string{"0", "2", "a", "b"},
			B:          []string{"2", "5"},
			insertCost: 1,
			deleteCost: 1,
			expected:   3,
		},
		{
			name:       "Sample Input 2",
			A:          []string{"2", "a", "b"},
			B:          []string{"0", "3", "1"},
			insertCost: 1,
			deleteCost: 1,
			expected:   3,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			require.Equal(t, tt.expected, dp.MinTransformationCost(tt.A, tt.B, tt.insertCost, tt.deleteCost))
		})
	}
}
