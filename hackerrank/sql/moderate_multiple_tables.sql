/*
https://www.hackerrank.com/challenges/the-company

Given the table schemas below, write a query to print the company_code, founder name, total number of lead managers, total number of senior managers, 
total number of managers, and total number of employees. Order your output by ascending company_code.

MySQL
*/

#	first solution: multiple joins
SELECT comp.company_code, comp.founder, COUNT(DISTINCT lmc), COUNT(DISTINCT smc), COUNT(DISTINCT mc), COUNT(DISTINCT ec) FROM COMPANY comp
INNER JOIN (SELECT lead_manager_code as lmc, company_code FROM Lead_Manager) AS lm
INNER JOIN (SELECT senior_manager_code as smc, company_code FROM Senior_Manager) AS sm
INNER JOIN (SELECT manager_code as mc, company_code FROM Manager) AS mng
INNER JOIN (SELECT employee_code as ec, company_code FROM Employee) AS empl
ON lm.company_code = comp.company_code AND sm.company_code = comp.company_code AND mng.company_code = comp.company_code AND empl.company_code = comp.company_code
GROUP BY comp.company_code

#	second solution: no joins, all the data is already in the last table, Employee
SELECT Company.company_code, founder, COUNT(distinct lead_manager_code), COUNT(distinct senior_manager_code), COUNT(distinct manager_code), COUNT(distinct employee_code) FROM Employee,Company 
WHERE Employee.company_code = Company.Company_Code GROUP BY company_code ORDER BY company_code