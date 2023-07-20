-- TODO: This query will return a table with two columns; order_status, and
-- Ammount. The first one will have the different order status classes and the
-- second one the total ammount of each.

select order_status, count(order_status) as Ammount
from olist_orders 
group by order_status 

