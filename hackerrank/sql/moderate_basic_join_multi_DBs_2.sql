/*
https://www.hackerrank.com/challenges/full-score

 Write a query to print the respective hacker_id and name of hackers who achieved full scores for more than one challenge.

DB2, Oracle, MySQL, MS SQL Server
*/

-- variant 1: using WHERE outside the inner SELECT
SELECT hacker_id, name FROM Hackers
INNER JOIN
(
    SELECT Submissions.hacker_id as hid, COUNT(Submissions.hacker_id) as cnt FROM Submissions
    INNER JOIN Challenges ON Challenges.challenge_id = Submissions.challenge_id
    INNER JOIN Difficulty ON Challenges.difficulty_level = Difficulty.difficulty_level
    WHERE Difficulty.Score = Submissions.Score
    GROUP BY Submissions.hacker_id
) selection ON selection.hid = Hackers.hacker_id
WHERE selection.cnt > 1
ORDER BY cnt DESC, Hackers.hacker_id ASC;

-- variant 2: using HAVING inside the inner SELECT (should be faster especially if the COUNT is done only once)
-- MySQL: using HAVING, only on MySQL with alias (unknown 'cnt' in HAVING)
-- it works if we do not use the alias: DB2, Oracle, MS SQL Server
SELECT hacker_id, name FROM Hackers
INNER JOIN
(
    SELECT Submissions.hacker_id as hid, COUNT(Submissions.hacker_id) as cnt FROM Submissions
    INNER JOIN Challenges ON Challenges.challenge_id = Submissions.challenge_id
    INNER JOIN Difficulty ON Challenges.difficulty_level = Difficulty.difficulty_level
    WHERE Difficulty.Score = Submissions.Score
    GROUP BY Submissions.hacker_id HAVING COUNT(Submissions.hacker_id) > 1
) selection ON selection.hid = Hackers.hacker_id
ORDER BY cnt DESC, Hackers.hacker_id ASC;