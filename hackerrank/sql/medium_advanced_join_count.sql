/*
https://www.hackerrank.com/challenges/symmetric-pairs

f(f(X)) = X, but 2 lines if f(X) = X
*/

-- SQLite, MS SQL Server: %; MySQL, Oracle, DB2: MOD
SELECT X, Y FROM Functions
WHERE X = Y 
-- MS SQL Server: "Column 'Functions.Y' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause."
-- Oracle does not know '%' operator
-- GROUP BY X,Y HAVING COUNT(X) % 2 = 0
GROUP BY X,Y HAVING MOD(COUNT(X),2) = 0
UNION
SELECT f.X, f.Y FROM Functions f
INNER JOIN Functions g ON f.Y = g.X AND f.X = g.Y 
WHERE f.X < f.Y
ORDER BY X;
