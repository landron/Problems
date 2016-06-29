/*
 Binary Search Tree
https://www.hackerrank.com/challenges/binary-search-tree-1

MySQL
*/

#	first solution: inner select
SELECT N,
(
    CASE
        WHEN P IS NULL THEN "Root"
        WHEN N IN (SELECT DISTINCT P FROM BST) THEN "Inner"
        ELSE "Leaf"
    END
)
FROM BST ORDER BY N

#	second solution: discussions inspired, using COUNT with condition => more efficient if indexed on N
SELECT N,
(
    CASE
        WHEN P IS NULL THEN "Root"
        WHEN (SELECT COUNT(1) FROM BST WHERE P = b.N) = 0 THEN "Leaf"
        ELSE "Inner"
    END
)
FROM BST b ORDER BY N