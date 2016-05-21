/*
http://www.hackerrank.com/challenges/what-type-of-triangle
Write a query identifying the type of each record in the TRIANGLES table using its three side lengths.

MySQL
*/

SELECT
(
    CASE
        WHEN t.A = t.B and t.B = t.C THEN "Equilateral"
        WHEN t.A + t.B <= t.C OR t.A + t.C <= t.B OR t.C + t.B <= t.A THEN "Not A Triangle"
        WHEN t.A = t.B or t.B = t.C or t.A = t.C THEN "Isosceles"
        ELSE "Scalene"
    END
)
FROM TRIANGLES t;