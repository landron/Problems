/*
https://www.hackerrank.com/challenges/challenges

Write a query to print the hacker_id, name, and the total number of challenges created by each student. 
Sort your results by the total number of challenges in descending order. If more than one student created the same number of challenges, 
then sort the result by hacker_id. If more than one student created the same number of challenges and the count is less than the maximum 
number of challenges created, then exclude those students from the result.
*/

-- SQLite, MySQL, MS SQL Server, DB2, Oracle
SELECT Hackers.hacker_id, Hackers.name, sel.total FROM Hackers
INNER JOIN
(
    -- Hackers.hacker_id necessary here as used in GROUP BY
    SELECT COUNT(Challenges.challenge_id) AS total, Hackers.hacker_id AS hacker_id FROM Challenges
    INNER JOIN Hackers ON Hackers.hacker_id = Challenges.hacker_id
    GROUP BY Hackers.hacker_id
) sel ON Hackers.hacker_id = sel.hacker_id 
INNER JOIN
(
	SELECT COUNT(sel.total) AS count, sel.total AS total FROM Hackers
	INNER JOIN
	(
	    SELECT COUNT(Challenges.challenge_id) AS total, Hackers.hacker_id AS hacker_id FROM Challenges
	    INNER JOIN Hackers ON Hackers.hacker_id = Challenges.hacker_id
	    GROUP BY Hackers.hacker_id
	) sel ON Hackers.hacker_id = sel.hacker_id 
	GROUP BY sel.total
) stats ON stats.total = sel.total
WHERE stats.count = 1 OR sel.total = (SELECT MAX(total) FROM (SELECT COUNT(Challenges.challenge_id) AS total FROM Challenges GROUP BY Challenges.hacker_id) counts)
ORDER BY sel.total DESC, Hackers.hacker_id;