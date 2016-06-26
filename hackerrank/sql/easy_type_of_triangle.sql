/*
http://www.hackerrank.com/challenges/what-type-of-triangle
Write a query identifying the type of each record in the TRIANGLES table using its three side lengths.

MySQL
*/

SELECT
(
    CASE
        WHEN A = B and B = C THEN "Equilateral"
        WHEN A + B <= C OR A + C <= B OR C + B <= A THEN "Not A Triangle"
        WHEN A = B or B = C or A = C THEN "Isosceles"
        ELSE "Scalene"
    END
)
FROM TRIANGLES;