/*
http://www.hackerrank.com/challenges/weather-observation-station-20

A median is defined as a number separating the higher half of a data set from the lower half. Query the median of the Northern Latitudes (LAT_N)
from STATION and round your answer to 4 decimal places.

MySQL

83.8913: does it always work?
*/

SET @rank=0;
SELECT ROUND(s.LAT_N,4) FROM STATION s 
INNER JOIN (SELECT s.LAT_N, @rank:=@rank+1 as rank FROM STATION s 
			INNER JOIN (SELECT LAT_N FROM STATION ORDER BY LAT_N ASC) AS t ON s.LAT_N = t.LAT_N) 
as t ON s.LAT_N = t.LAT_N AND t.rank = (SELECT CEIL(COUNT(*)/2) FROM STATION)