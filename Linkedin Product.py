Sold quantity on three products
You have the following table with the quantity of product A, B, and C sold per day.

date	qty_prod_a	qty_prod_b	qty_prod_c
1/1/2013	100	200	300
1/2/2013	101	0	301
1/3/2013	102	202	302
There are only 3 possible product in the table: A, B and C. Write SQL code to reformat the data
above and the resulting data should be in 3 columns {date, product name, quantity sold}.


select
date
, A as product_name
, qty_prod_a as quantity_sold
from sales
where qty_prod_a > 0

union

select
, B as product_name
, qty_prod_b as quantity_sold
from sales
where qty_prod_b > 0

union

select
, C as product_name
, qty_prod_c as quantity_sold
from sales
where qty_prod_c > 0
;