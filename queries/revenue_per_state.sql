-- TODO: This query will return a table with two columns; customer_state, and 
-- Revenue. The first one will have the letters that identify the top 10 states 
-- with most revenue and the second one the total revenue of each.
-- HINT: All orders should have a delivered status and the actual delivery date 
-- should be not null. 

select c.customer_state, sum(p.payment_value) as Revenue
from olist_customers as c, olist_orders as o, olist_order_payments as p
where p.order_id = o.order_id and o.customer_id = c.customer_id 
and o.order_delivered_customer_date is not null and o.order_status = 'delivered'
group by c.customer_state 
order by Revenue desc
limit 10