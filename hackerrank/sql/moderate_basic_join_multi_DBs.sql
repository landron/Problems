/*
https://www.hackerrank.com/challenges/the-report

The report must be in descending order by grade -- i.e. higher grades are entered first. If there is more than one student with the same grade (1-10)
assigned to them, order those particular students by their name alphabetically. Finally, if the grade is lower than 8, use "NULL" as their name and
list them by their marks in ascending order.

DB2, Oracle, MySQL, MS SQL Server
*/

SELECT (CASE WHEN grades.Grade >= 8 THEN Name ELSE 'NULL' END), grades.Grade, Students.Marks FROM Students 
INNER JOIN (SELECT * FROM Grades) grades 
ON Students.Marks >= grades.Min_Mark AND Students.Marks <= grades.Max_Mark 
ORDER BY grades.Grade DESC, Students.Name ASC;