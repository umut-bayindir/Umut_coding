

-- Employee (SSN, FName, MInit, LName, Address, Sex, Salary, Super SSN, DNo)
-- Dept Location(DNumber, DLocation)
-- Department(DNumber, DName, MgrSSN )
-- Project(PNumber, PName, PLocation, DNum)
-- WorksOn( ESSN, PNo, Hours)
-- Dependant(ESSN, dependent name, Sex, BDate, Relationship)

--1. List the names of all the projects done by the company.
SELECT PName FROM Project;
--tested successfully
-- 2. For "Franklin Wong", list all the projects he works on and the hours he works on each project.
SELECT Pname,hours FROM Employee, works_on, Project WHERE SSN = ESSN and Fname = 'Frank' and PNumber = PNo;
--tested successfully
-- 3. List the names of all employees who work on project #20.
SELECT DISTINCT FName, LName FROM Employee, works_on WHERE SSN = ESSN and PNo = 20;
--tested successfully
-- 4. List the names of all employees who work on project #20 or project #30.
SELECT DISTINCT FName, LName FROM Employee, works_on WHERE SSN = ESSN and PNo = 20 or PNo = 30;
--tested successfully
-- 5. List the names of all employees who work on project #10 for 10 or more hours.
SELECT DISTINCT FName, LName FROM Employee, works_on WHERE SSN = ESSN and PNo = 10 and Hours = 10;
--tested successfully
-- 6. List the names of all employees who have at least 2 dependants.
SELECT DISTINCT e.fname, e.lname
FROM employee e
JOIN dependent d ON e.ssn = d.essn
GROUP BY e.ssn
HAVING COUNT(d.dependent_name) >= 2; 
--tested successfully
-- 7. List the names of all employees with no dependants.
SELECT DISTINCT e.fname, e.lname
FROM employee e
LEFT JOIN dependent d ON e.ssn = d.essn
WHERE d.dependent_name IS NULL;
--tested successfully
-- 8. List the names of all employees who work on one project only.
SELECT DISTINCT e.fname, e.lname
FROM employee e
JOIN works_on w ON e.ssn = w.essn
GROUP BY e.ssn
HAVING COUNT(w.pno) = 1; 
-- tested successfully
-- 9. List the names of all employees who work on projects controlled by the "Administration"
-- Department.
SELECT DISTINCT e.fname, e.lname
FROM employee e
JOIN works_on w ON e.ssn = w.essn
JOIN project p ON w.pno = p.pnumber
JOIN department d ON p.dnum = d.dnumber
WHERE d.dname = 'Administration';
--tested successfully
-- 10. List all projects that have employees working 10 or more hours
SELECT DISTINCT p.pname
FROM project p
JOIN works_on w ON p.pnumber = w.pno
GROUP BY p.pnumber
HAVING SUM(w.hours) >= 10;
--tested successfully





