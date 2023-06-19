-- TODO: This query will return a table with the differences between the real 
-- and estimated delivery times by month and year. It will have different 
-- columns: month_no, with the month numbers going from 01 to 12; month, with 
-- the 3 first letters of each month (e.g. Jan, Feb); Year2016_real_time, with 
-- the average delivery time per month of 2016 (NaN if it doesn't exist); 
-- Year2017_real_time, with the average delivery time per month of 2017 (NaN if 
-- it doesn't exist); Year2018_real_time, with the average delivery time per 
-- month of 2018 (NaN if it doesn't exist); Year2016_estimated_time, with the 
-- average estimated delivery time per month of 2016 (NaN if it doesn't exist); 
-- Year2017_estimated_time, with the average estimated delivery time per month 
-- of 2017 (NaN if it doesn't exist) and Year2018_estimated_time, with the 
-- average estimated delivery time per month of 2018 (NaN if it doesn't exist).
-- HINTS
-- 1. You can use the julianday function to convert a date to a number.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Take distinct order_id.

SELECT
	strftime('%m', oo.order_purchase_timestamp) AS month_no,
	substr ("--JanFebMarAprMayJunJulAugSepOctNovDec", STRFTIME("%m", oo.order_purchase_timestamp) * 3, 3) as "month",
	avg(iif(strftime('%Y', oo.order_purchase_timestamp) = '2016', julianday(oo.order_delivered_customer_date) - julianday(oo.order_purchase_timestamp), null)) AS Year2016_real_time,
	avg(iif(strftime('%Y', oo.order_purchase_timestamp) = '2017', julianday(oo.order_delivered_customer_date) - julianday(oo.order_purchase_timestamp), null)) AS Year2017_real_time,
	avg(iif(strftime('%Y', oo.order_purchase_timestamp) = '2018', julianday(oo.order_delivered_customer_date) - julianday(oo.order_purchase_timestamp), null)) AS Year2018_real_time,
	avg(iif(strftime('%Y', oo.order_purchase_timestamp) = '2016', julianday(oo.order_estimated_delivery_date) - julianday(oo.order_purchase_timestamp), null)) AS Year2016_estimated_time,
	avg(iif(strftime('%Y', oo.order_purchase_timestamp) = '2017', julianday(oo.order_estimated_delivery_date) - julianday(oo.order_purchase_timestamp), null)) AS Year2017_estimated_time,
	avg(iif(strftime('%Y', oo.order_purchase_timestamp) = '2018', julianday(oo.order_estimated_delivery_date) - julianday(oo.order_purchase_timestamp), null)) AS Year2018_estimated_time
FROM
	olist_orders AS oo
WHERE
	order_status = 'delivered'
	AND order_delivered_customer_date IS NOT NULL
GROUP BY
	month_no;