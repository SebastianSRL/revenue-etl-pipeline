from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy import text
from sqlalchemy.engine.base import Engine

from src.config import QUERIES_ROOT_PATH

QueryResult = namedtuple("QueryResult", ["query", "result"])


class QueryEnum(Enum):
    """This class enumerates all the queries that are available"""

    DELIVERY_DATE_DIFFERECE = "delivery_date_difference"
    GLOBAL_AMMOUNT_ORDER_STATUS = "global_ammount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"


def read_query(query_name: str) -> str:
    """Read the query from the file.

    Args:
        query_name (str): The name of the file.

    Returns:
        str: The query.
    """
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql_file = f.read()
        sql = text(sql_file)
    return sql


def query_delivery_date_difference(database: Engine) -> QueryResult:
    """Get the query for delivery date difference.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for delivery date difference.
    """
    query_name = QueryEnum.DELIVERY_DATE_DIFFERECE.value
    query = read_query(QueryEnum.DELIVERY_DATE_DIFFERECE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_global_ammount_order_status(database: Engine) -> QueryResult:
    """Get the query for global amount of order status.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for global percentage of order status.
    """
    query_name = QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value
    query = read_query(QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_by_month_year(database: Engine) -> QueryResult:
    """Get the query for revenue by month year.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for revenue by month year.
    """
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(QueryEnum.REVENUE_BY_MONTH_YEAR.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_per_state(database: Engine) -> QueryResult:
    """Get the query for revenue per state.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for revenue per state.
    """
    query_name = QueryEnum.REVENUE_PER_STATE.value
    query = read_query(QueryEnum.REVENUE_PER_STATE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    """Get the query for top 10 least revenue categories.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for top 10 least revenue categories.
    """
    query_name = QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value
    query = read_query(QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    """Get the query for top 10 revenue categories.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for top 10 revenue categories.
    """
    query_name = QueryEnum.TOP_10_REVENUE_CATEGORIES.value
    query = read_query(QueryEnum.TOP_10_REVENUE_CATEGORIES.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    """Get the query for real vs estimated delivered time.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for real vs estimated delivered time.
    """
    query_name = QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value
    query = read_query(QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    """Get the freight_value weight relation for delivered orders.

    In this particular query, we want to evaluate if exists a correlation between
    the weight of the product and the value paid for delivery.

    We will use olist_orders, olist_order_items, and olist_products tables alongside
    some Pandas magic to produce the desired output: A table that allows us to
    compare the order total weight and total freight value.

    Of course, you could also do this with pure SQL statements but we would like
    to see if you've learned correctly the pandas' concepts seen so far.

    Args:
        database (Engine): Database connection.

    Returns:
        QueryResult: The query for freight_value vs weight data.
    """
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value

    # Get orders from olist_orders table
    orders = read_sql("SELECT * FROM olist_orders", database)

    # Get items from olist_order_items table
    items = read_sql("SELECT * FROM olist_order_items", database)

    # Get products from olist_products table
    products = read_sql("SELECT * FROM olist_products", database)

    # TODO: Merge items, orders and products tables on 'order_id'/'product_id'.
    # We suggest to use pandas.merge() function.
    # Assign the result to the `data` variable.
    data = items.merge(products, on="product_id").merge(orders, on="order_id")
    # TODO: Get only delivered orders.
    # Using the previous results from the merge (stored in `data` variable),
    # apply a boolean mask to keep only the 'delivered' orders.
    # Assign the result to the variable `delivered`.
    delivered = data[data.order_status == "delivered"]

    # TODO: Get the sum of freight_value and product_weight_g for each order_id.
    # The same order (identified by 'order_id') can have multiple products inside,
    # then we decided to sum all the products 'freight_value' and 'product_weight_g'
    # inside that order.
    # Use the pandas DataFrame stored in `delivered` variable. We suggest you to
    # look at pandas.DataFrame.groupby() and pandas.DataFrame.agg() for the data
    # transformation.
    # Store the result in the `aggregations` variable.
    aggregations = (
        delivered.groupby(["order_id"])[["freight_value", "product_weight_g"]]
        .agg(sum)
        .reset_index()
    )

    # Keep the code below as it is, this will return the result from
    # `aggregations` variable with the corresponding name and format.
    return QueryResult(query=query_name, result=aggregations)


def query_orders_per_day_and_holidays_2017(database: Engine) -> QueryResult:
    """Get the query for orders per day and holidays in 2017.

    In this query, we want to get a table with the relation between the number
    of orders made on each day and also information that indicates if that day was
    a Holiday.

    Of course, you could also do this with pure SQL statements but we would like
    to see if you've learned correctly the pandas' concepts seen so far.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for orders per day and holidays in 2017.
    """
    query_name = QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value

    # Reading the public holidays from public_holidays table
    holidays = read_sql("SELECT * FROM public_holidays", database)

    # Reading the orders from olist_orders table
    orders = read_sql("SELECT * FROM olist_orders", database)

    # TODO: Converting the order_purchase_timestamp column to datetime.
    # Replace the content for the column `order_purchase_timestamp` in the `orders`
    # DataFrame with the same data but converted to datetime.
    # We suggest you to read about how to use pd.to_datetime() for this.
    orders["order_purchase_timestamp"] = pd.to_datetime(orders.order_purchase_timestamp)
    # TODO: Filtering only the order purchase timestamps from the year 2017.
    # Using the `orders` DataFrame, apply a boolean mask for retrieving all the
    # columns but only the rows corresponding to the year 2017.
    # Assign the result to a new variable called `filtered_dates`.
    filtered_dates = orders[orders.order_purchase_timestamp.dt.year == 2017]

    # TODO: Counting the orders per day.
    # Using the `filtered_dates` DataFrame, count how many orders were made on
    # each day.
    # Assign the result to the `order_purchase_ammount_per_date` variable.

    filtered_dates.order_purchase_timestamp = (
        filtered_dates.order_purchase_timestamp.dt.date
    )
    order_purchase_ammount_per_date = (
        filtered_dates.groupby("order_purchase_timestamp")
        .agg({"order_id": "count"})
        .reset_index()
    )

    # TODO: Creating a dataframe with the result. Assign it to `result_df` variable.
    # Now we will create the final DataFrame for the output.
    # This DataFrame must have 3 columns:
    #   - 'order_count': with the number of orders per day, you should be able to get
    #                    this data from `order_purchase_ammount_per_date` variable.
    #   - 'date': the corresponding date for each count of orders.
    #   - 'holiday': boolean column having True when that date is a holiday or,
    #                False otherwise. Use the `hlidays` DataFrame for this.
    result_df = pd.DataFrame(
        {
            "order_count": order_purchase_ammount_per_date.order_id,
            "date": order_purchase_ammount_per_date.order_purchase_timestamp,
            "holiday": order_purchase_ammount_per_date.order_purchase_timestamp.isin(
                pd.to_datetime(holidays.date).dt.date
            ),
        }
    )

    # Keep the code below as it is, this will return the result from
    # `aggregations` variable with the corresponding name and format.
    return QueryResult(query=query_name, result=result_df)


def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    """Get all queries.

    Returns:
        List[Callable[[Engine], QueryResult]]: A list of all queries.
    """
    return [
        query_delivery_date_difference,
        query_global_ammount_order_status,
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]


def run_queries(database: Engine) -> Dict[str, DataFrame]:
    """Transform data based on the queries. For each query, the query is executed and
    the result is stored in the dataframe.

    Args:
        database (Engine): Database connection.

    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the query file names and
        values the result of the query as a dataframe.
    """
    query_results = {}
    for query in get_all_queries():
        query_result = query(database)
        query_results[query_result.query] = query_result.result
    return query_results
