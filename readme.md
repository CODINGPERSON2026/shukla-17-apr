# TO RUN THIS APPLICATION 
 follow the steps

## 1.open HRMS into into vs code
## 2. Press ctrl + j (terminal will open)

#  Paste the below line as it is
## waitress-serve --host=127.0.0.1 --port=4000 app:app  and Press enter

SELECT p.army_number
FROM personnel p
LEFT JOIN weight_info w 
    ON p.army_number = w.army_number
WHERE w.army_number IS NULL;



use copy_hrms;
insert into hrms.weight_info 
(army_number,`rank`,name,actual_weight,height,company,age)
select p.army_number,
p.`rank`,
p.name,
p.actual_weight,
p.height,
p.company,
timestampdiff(YEAR,p.date_of_birth,curdate()) as age
from personnel p where p.army_number = ''




select p.army_number from personnel p where not exists (select 1 from weight_info w where w.army_number = p.army_number)


## this below is for copying all daata from personnel to weight_info for fixingin mismatch
insert into hrms.weight_info 
(army_number,`rank`,name,actual_weight,height,company,age)
select p.army_number,
p.`rank`,
p.name,
p.weight,
p.height,
p.company,
timestampdiff(YEAR,p.date_of_birth,curdate()) as age
from hrms.personnel p where not exists (SELECT 1 FROM hrms.weight_info w where w.army_number = p.army_number);






