/*
https://www.hackerrank.com/challenges/harry-potter-and-wands

 Write a query to print the id, age, coins_needed, and power of the wands that Ron's interested in, sorted in order of descending power. 
 If more than one wand has same power, sort the result in order of descending age.
    Same power & age => sort by coins needed

DB2, Oracle, MySQL, MS SQL Server
*/

-- MySQL: SELECT works even for fields not specified in GROUP BY/aggregate function
SELECT Wands.id, sel.age, Wands.coins_needed, Wands.power FROM Wands
INNER JOIN
(
    SELECT Min(Wands.coins_needed) as coins_needed, Wands.code as code, Wands_Property.age as age FROM Wands 
    INNER JOIN Wands_Property ON Wands_Property.code = Wands.code AND NOT Wands_Property.is_evil 
    GROUP BY Wands.power, Wands_Property.age
    ORDER BY Wands.power DESC, Wands_Property.age DESC
) sel ON sel.coins_needed = Wands.coins_needed AND sel.code = Wands.code
GROUP BY Wands.power, sel.age
ORDER BY Wands.power DESC, sel.age DESC

-- variant 2: the previous simplified to have it work
-- MySQL, MS SQL Server, Oracle, DB2
SELECT Wands.id, sel.age, Wands.coins_needed, Wands.power FROM Wands
INNER JOIN
(
    SELECT Min(Wands.coins_needed) as coins_needed, Wands.code as code, Wands_Property.age as age FROM Wands 
    INNER JOIN Wands_Property ON Wands_Property.code = Wands.code AND Wands_Property.is_evil = 0
    GROUP BY Wands.power, Wands_Property.age, Wands.code
) sel ON sel.coins_needed = Wands.coins_needed AND sel.code = Wands.code
ORDER BY Wands.power DESC, sel.age DESC;