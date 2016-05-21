/*
http://www.hackerrank.com/challenges/weather-observation-station-15
Query the Western Longitude (LONG_W) for the largest Northern Latitude (LAT_N) in STATION that is less than 137.2345. Round your answer to  decimal places.

MySQL
*/

SELECT ROUND(s.LONG_W,4) FROM STATION s JOIN (SELECT MAX(LAT_N) as max FROM STATION t WHERE t.LAT_N < 137.2345) AS t ON s.LAT_N = t.max