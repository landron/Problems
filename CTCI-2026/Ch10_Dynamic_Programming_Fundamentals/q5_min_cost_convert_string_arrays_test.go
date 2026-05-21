/*
go test -c ./Ch10_Dynamic_Programming_Fundamentals
*/
package main

import "testing"

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
			expected:   0,
		},
		{
			name:       "Sample Input 1",
			A:          []string{"0", "2", "a", "b"},
			B:          []string{"2", "5"},
			insertCost: 1,
			deleteCost: 1,
			expected:   4,
		},
		{
			name:       "Sample Input 2",
			A:          []string{"2", "a", "b"},
			B:          []string{"0", "3", "1"},
			insertCost: 1,
			deleteCost: 1,
			expected:   2,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := minTransformationCost(tt.A, tt.B, tt.insertCost, tt.deleteCost)
			if actual != tt.expected {
				t.Errorf("minTransformationCost() = %d; want %d", actual, tt.expected)
			}
		})
	}
}
