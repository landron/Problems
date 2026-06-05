/*
Min Cost to Convert String Arrays with Edit Distance

	Implement a function that Minimum total cost to transform A into B
	using insertions, deletions, and line modifications.

https://www.hackerrank.com/contests/software-engineer-prep-kit/challenges/min-cost-convert-string-arrays-edit-distance

Solution

	Gemini: The core idea is to use Dynamic Programming, specifically a variant
	of the Levenshtein Edit Distance algorithm applied to arrays of strings
	(lines) instead of individual characters.

#algo_dp
#dp_2d_grid
#dp_string
#classic_edit_distance
#pattern_prefix_dp
#space_optimizable
*/
package dynamic_programming

import "fmt"

/*
 * Complete the 'minTransformationCost' function below.
 *
 * The function is expected to return a LONG_INTEGER.
 * The function accepts following parameters:
 *  1. STRING_ARRAY a
 *  2. STRING_ARRAY b
 *  3. INTEGER insertCost
 *  4. INTEGER deleteCost
 */

func MinTransformationCost(a, b []string, insertCost, deleteCost int32) int64 {
	m, n := len(a), len(b)
	dp := make([][]int64, m+1)
	for i := range dp {
		dp[i] = make([]int64, n+1)
		dp[i][0] = int64(i) * int64(deleteCost) // Beware!
	}
	for j := 0; j <= n; j++ {
		dp[0][j] = int64(j) * int64(insertCost)
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				dp[i][j] = dp[i-1][j-1]
			} else {
				// replace := dp[i-1][j-1] + min(
				// 	int64(deleteCost+insertCost),
				// 	int64(EditCostBottomUp(a[i-1], b[j-1])),
				// )
				dp[i][j] = min(
					dp[i-1][j]+int64(deleteCost),                         // delete
					dp[i][j-1]+int64(insertCost),                         // insert
					dp[i-1][j-1]+int64(EditCostBottomUp(a[i-1], b[j-1])), // edit
					// replace,
				)
			}
		}
	}

	// PrintArrayMatrix(a,b,dp)
	return dp[m][n]
}

func EditCostBottomUp(source, target string) int {
	m, n := len(source), len(target)
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
		dp[i][0] = i
	}
	for j := 0; j <= n; j++ {
		dp[0][j] = j
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if source[i-1] == target[j-1] {
				dp[i][j] = dp[i-1][j-1]
			} else {
				dp[i][j] = 1 + min(
					dp[i-1][j],   // delete
					dp[i][j-1],   // insert
					dp[i-1][j-1], // replace
				)
			}
		}
	}

	return dp[m][n]
}

func EditCostTopDown(source, target string) int {
	/*
		len(source)+1: first line & column are initialized
	*/
	memo := make([][]int, len(source)+1)
	for i := range memo {
		memo[i] = make([]int, len(target)+1)
		for j := range memo[i] {
			memo[i][j] = -1
		}
		// memo[i][0] = i
	}
	// for i := range len(target) {
	// 	memo[0][i] = i
	// }

	return costTopDown(len(source), len(target), source, target, memo)
}

func costTopDown(i, j int, s, t string, memo [][]int) int {
	if i == 0 {
		return j
	}
	if j == 0 {
		return i
	}
	if memo[i][j] != -1 {
		return memo[i][j]
	}

	solution := 0
	// we actually check -1:
	// 	memo index is in advance and goes to lengths of s,t
	if s[i-1] == t[j-1] {
		solution = costTopDown(i-1, j-1, s, t, memo)
	} else {
		solution = 1 + min(
			costTopDown(i-1, j, s, t, memo),   // delete
			costTopDown(i, j-1, s, t, memo),   // insert
			costTopDown(i-1, j-1, s, t, memo), // replace
		)
	}
	memo[i][j] = solution

	return solution
}

// PrintMatrix prints the DP table with string row/column headers for debugging
func PrintMatrix(source, target string, matrix [][]int) {
	// Print top target header
	fmt.Print("      ")
	for j := 0; j < len(target); j++ {
		fmt.Printf("%3c ", target[j])
	}
	fmt.Println()

	// Print the rows
	for i := 0; i < len(matrix); i++ {
		// Print side source header
		if i == 0 {
			fmt.Print("  ")
		} else {
			fmt.Printf("%c ", source[i-1])
		}

		// Print row values
		for j := 0; j < len(matrix[i]); j++ {
			fmt.Printf("%3d ", matrix[i][j])
		}
		fmt.Println()
	}
}

// PrintArrayMatrix prints the outer DP table with string slice headers
func PrintArrayMatrix(source, target []string, matrix [][]int64) {
	// Find the longest string in target to dynamically set column width
	maxWidth := 4
	for _, s := range target {
		if len(s) > maxWidth {
			maxWidth = len(s)
		}
	}
	formatStr := fmt.Sprintf("%%%ds ", maxWidth)

	// Print top target header
	fmt.Printf(formatStr, "")  // top-left empty corner
	fmt.Printf(formatStr, "∅") // base case column
	for j := 0; j < len(target); j++ {
		fmt.Printf(formatStr, target[j])
	}
	fmt.Println()

	// Print the rows
	for i := 0; i < len(matrix); i++ {
		// Print side source header
		if i == 0 {
			fmt.Printf(formatStr, "∅")
		} else {
			fmt.Printf(formatStr, source[i-1])
		}

		// Print row values
		for j := 0; j < len(matrix[i]); j++ {
			fmt.Printf(formatStr, fmt.Sprintf("%d", matrix[i][j]))
		}
		fmt.Println()
	}
}
