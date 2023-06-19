-- TODO: This query will return a table with the top 10 revenue categories in 
-- English, the number of orders and their total revenue. The first column will 
-- be Category, that will contain the top 10 revenue categories; the second one 
-- will be Num_order, with the total amount of orders of each category; and the 
-- last one will be Revenue, with the total revenue of each catgory.
-- HINT: All orders should have a delivered status and the Category and actual 
-- delivery date should be not null.


--working
select n.product_category_name_english as Category, count(DISTINCT order_id) as Num_order, sum(oop.payment_value) as Revenue from olist_order_items ooi
inner join olist_products op using(product_id)
inner join olist_order_payments oop using(order_id)
inner join olist_orders oo using(order_id)
join product_category_name_translation n using(product_category_name)
where oo.order_status = 'delivered'
and oo.order_delivered_customer_date is not null  
and Category is not null
group by op.product_category_name 
order by Revenue desc 
limit 10