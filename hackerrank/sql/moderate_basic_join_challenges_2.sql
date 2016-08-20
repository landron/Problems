/*
https://www.hackerrank.com/challenges/contest-leaderboard

Write a query to print the hacker_id, name, and total score of the hackers ordered by the descending score. 
If more than one hacker achieved the same total score, then sort the result by ascending hacker_id. 
Exclude all hackers with a total score of  0 from your result.
*/

-- SQLite, MySQL, MS SQL Server, Oracle, DB2
SELECT Hackers.hacker_id, Hackers.name, SUM(scores.max_score) AS sum_scores FROM Hackers
INNER JOIN
(
    SELECT Hackers.hacker_id as hacker_id, MAX(Submissions.score) AS max_score FROM Hackers
    INNER JOIN Submissions ON Submissions.hacker_id = Hackers.hacker_id
    GROUP BY Submissions.challenge_id, Hackers.hacker_id HAVING MAX(Submissions.score) <> 0
) scores ON scores.hacker_id = Hackers.hacker_id
/*
    MS SQL Server: Column 'Hackers.name' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause. 
    \todo: find a better solution
*/
GROUP BY Hackers.hacker_id, Hackers.name HAVING SUM(scores.max_score) <> 0
ORDER BY sum_scores DESC, Hackers.hacker_id;