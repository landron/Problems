/*
https://www.hackerrank.com/challenges/the-blunder

MySQL
*/

SELECT 1+ROUND(AVG(SALARY)-AVG(CONVERT(REPLACE(CONVERT(SALARY, char), "0", ""), UNSIGNED))) FROM EMPLOYEES