/*
https://www.hackerrank.com/challenges/average-population-of-each-continent

Given the CITY and COUNTRY tables, query the names of all the continents (COUNTRY.Continent) and their respective average city populations (CITY.Population) 
rounded down to the nearest integer.

MySQL
*/

SELECT country.continent, FLOOR(AVG(city.population)) FROM COUNTRY country 
INNER JOIN (SELECT countrycode, population FROM CITY) AS city 
ON city.countrycode = country.code GROUP BY country.continent