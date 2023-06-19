-- TODO: This query will return a table with the revenue by month and year. It
-- will have different columns: month_no, with the month numbers going from 01
-- to 12; month, with the 3 first letters of each month (e.g. Jan, Feb);
-- Year2016, with the revenue per month of 2016 (0.00 if it doesn't exist);
-- Year2017, with the revenue per month of 2017 (0.00 if it doesn't exist) and
-- Year2018, with the revenue per month of 2018 (0.00 if it doesn't exist).

-- En teoría resuelve lo que piden hay un error en los resultados del test

-- select m as month_no, 
-- substr ("--JanFebMarAprMayJunJulAugSepOctNovDec", m * 3, 3) as "month",  
-- sum(iif((select rev where anio = '2016'), rev, 0)) as Year2016,
-- sum(iif((select rev where anio = '2017'), rev, 0)) as Year2017,
-- sum(iif((select rev where anio = '2018'), rev, 0)) as Year2018
-- from
-- (
-- 	select strftime('%m', o.order_delivered_customer_date) as m, 
-- 	strftime('%Y', o.order_delivered_customer_date) as anio, 
-- 	sum(p.payment_value) as rev
-- 	from olist_orders as o
-- 	join olist_order_payments p using(order_id)
-- 	where o.order_delivered_customer_date is not null
-- 	and o.order_status = 'delivered'
-- 	group by m, anio
-- )
-- group by month_no


SELECT STRFTIME('%m', oo.order_delivered_customer_date) as month_no,
CASE STRFTIME('%m', oo.order_delivered_customer_date)
    WHEN '01' THEN 'Jan'
    WHEN '02' THEN 'Feb' 
    WHEN '03' THEN 'Mar'
    WHEN '04' THEN 'Apr'
    WHEN '05' THEN 'May'
    WHEN '06' THEN 'Jun'
    WHEN '07' THEN 'Jul'
    WHEN '08' THEN 'Aug'
    WHEN '09' THEN 'Sep'
    WHEN '10' THEN 'Oct'
    WHEN '11' THEN 'Nov'
    WHEN '12' THEN 'Dec'
    ELSE 'Unknown'
END as month,
SUM(CASE WHEN STRFTIME('%Y', oo.order_delivered_customer_date) = '2016' THEN payments.order_sum END) AS 'Year2016',
SUM(CASE WHEN STRFTIME('%Y', oo.order_delivered_customer_date) = '2017' THEN payments.order_sum END) AS 'Year2017',
SUM(CASE WHEN STRFTIME('%Y', oo.order_delivered_customer_date) = '2018' THEN payments.order_sum END) AS 'Year2018'
FROM olist_orders oo
JOIN (
    SELECT p.order_id, MIN(p.payment_value) AS order_sum
    FROM olist_order_payments p
    GROUP BY p.order_id
) as payments
ON payments.order_id = oo.order_id
WHERE oo.order_status = 'delivered' AND oo.order_delivered_customer_date IS NOT NULL
GROUP BY month_no, month;