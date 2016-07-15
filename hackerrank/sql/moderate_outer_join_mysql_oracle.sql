/*
https://www.hackerrank.com/challenges/occupations

Pivot the Occupation column in OCCUPATIONS so that each Name is sorted alphabetically and displayed underneath its corresponding Occupation.
Note: Print NULL when there are no more names corresponding to an occupation.

MySQL, Oracle

\todo
2016/07/15:	the MySQL solution does not always work (UNION simulates FULL JOIN, but I didn't succeed to use it)
*/

# MySQL
SET @rd = 0, @rp = 0, @ra = 0, @rs = 0;
SELECT doc.Name, prof.Name, singer.Name, actor.Name From 
(
	(SELECT Name, @rp:=@rp+1 as rank FROM OCCUPATIONS WHERE Occupation = 'Professor' ORDER BY Name) as prof
    LEFT JOIN (SELECT Name, @ra:=@ra+1 as rank FROM OCCUPATIONS WHERE Occupation = 'Actor' ORDER BY Name) as actor ON prof.rank = actor.rank
    LEFT JOIN (SELECT Name, @rs:=@rs+1 as rank FROM OCCUPATIONS WHERE Occupation = 'Singer' ORDER BY Name) as singer ON actor.rank = singer.rank
    LEFT JOIN (SELECT Name, @rd:=@rd+1 as rank FROM OCCUPATIONS WHERE Occupation = 'Doctor' ORDER BY Name) as doc ON doc.rank = singer.rank
)

# Oracle
SELECT docs, profs, singers, actors From 
(
    (SELECT Name as docs, ROW_NUMBER() OVER(ORDER BY Name) as rank_d FROM OCCUPATIONS WHERE Occupation = 'Doctor')
    FULL JOIN (SELECT Name as profs, ROW_NUMBER() OVER(ORDER BY Name) as rank_p FROM OCCUPATIONS WHERE Occupation = 'Professor') ON rank_p = rank_d
    FULL JOIN (SELECT Name as singers, ROW_NUMBER() OVER(ORDER BY Name) as rank_s FROM OCCUPATIONS WHERE Occupation = 'Singer') ON rank_p = rank_s
    FULL JOIN (SELECT Name as actors, ROW_NUMBER() OVER(ORDER BY Name) as rank_a FROM OCCUPATIONS WHERE Occupation = 'Actor') ON rank_s = rank_a
);

#MySQL with no JOINS, by YujiShen 
set @r1=0, @r2=0, @r3=0, @r4=0;
select min(Doctor), min(Professor), min(Singer), min(Actor)
from(
  select case when Occupation='Doctor' then (@r1:=@r1+1)
            when Occupation='Professor' then (@r2:=@r2+1)
            when Occupation='Singer' then (@r3:=@r3+1)
            when Occupation='Actor' then (@r4:=@r4+1) end as RowNumber,
    case when Occupation='Doctor' then Name end as Doctor,
    case when Occupation='Professor' then Name end as Professor,
    case when Occupation='Singer' then Name end as Singer,
    case when Occupation='Actor' then Name end as Actor
  from OCCUPATIONS
  order by Name
) selection
group by RowNumber

#MS SQL Server (by francisstarr), inspired by the previous one
with cte as ( select RANK() OVER (PARTITION BY Occupation ORDER BY Name) as Rank, 
             case when Occupation='Doctor' then Name else null end as doctor, 
             case when Occupation='Professor' then Name else null end as prof, 
             case when Occupation='Singer' then Name else null end as singer, 
             case when Occupation='Actor' then Name else null end as actor from Occupations) 
select min(doctor), min(prof), min(singer), min(actor) from cte group by Rank


#MySQL (by gcastano1205)
/*
You did not explain how you fixed it: you took the row number from the 'Professor' selection (P), not the 'Doctor' one (D) so the line "NULL Maria Kristeen Samantha" looked like "NULL Maria NULL NULL".
  I am interested in your solution as it reassembles mine (as a perfectioned version :)), but this solution only works for the case when the 'Professor' selection is the biggest one. And that's because MySQL does not support FULL JOIN directly ("of course"), so I wonder if we can find a complete solution.
Thanks
*/
SELECT D.Name, P.Name, S.Name, A.Name FROM 
(
    (SELECT @rownum:=@rownum+1 AS rownum, Name FROM (SELECT @rownum:=0) r, Occupations WHERE Occupation = 'Doctor' ORDER BY Name) AS D 
    RIGHT JOIN (SELECT @rownumP:=@rownumP+1 AS rownum, Name FROM (SELECT @rownumP:=0) r, Occupations WHERE Occupation = 'Professor' ORDER BY Name) AS P ON D.rownum = P.rownum 
    LEFT JOIN (SELECT @rownumS:=@rownumS+1 AS rownum, Name FROM (SELECT @rownumS:=0) r, Occupations WHERE Occupation = 'Singer' ORDER BY Name) AS S ON P.rownum = S.rownum 
    LEFT JOIN (SELECT @rownumA:=@rownumA+1 AS rownum, Name FROM (SELECT @rownumA:=0) r, Occupations WHERE Occupation = 'Actor' ORDER BY Name) AS A ON P.rownum = A.rownum
);
