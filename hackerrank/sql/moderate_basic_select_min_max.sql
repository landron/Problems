/*
http://www.hackerrank.com/challenges/weather-observation-station-5

Query the two cities in STATION with the shortest and longest CITY names, as well as their respective lengths (i.e.: number of characters in the name). 
If there is more than one smallest or largest city, choose the one that comes first when ordered alphabetically.

MySQL
*/

SELECT CITY, LENGTH(CITY) FROM STATION s ORDER BY LENGTH(s.CITY) ASC, s.CITY LIMIT 1;
SELECT CITY, LENGTH(CITY) FROM STATION s ORDER BY LENGTH(s.CITY) DESC, s.CITY LIMIT 1;