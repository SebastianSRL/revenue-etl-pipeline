from src.config import DATASET_ROOT_PATH, PUBLIC_HOLIDAYS_URL, get_csv_to_table_mapping
from src.extract import extract, get_public_holidays


def test_get_public_holidays():
    """Test the get_public_holidays function."""
    year = "2017"
    public_holidays = get_public_holidays(PUBLIC_HOLIDAYS_URL, year)
    assert public_holidays.shape == (14, 7)
    assert public_holidays["date"].dtype == "datetime64[ns]"


def test_extract():
    """Test the extract function."""
    csv_folder = DATASET_ROOT_PATH
    csv_table_mapping = get_csv_to_table_mapping()
    public_holidays_url = PUBLIC_HOLIDAYS_URL
    dataframes = extract(csv_folder, csv_table_mapping, public_holidays_url)
    assert len(dataframes) == len(csv_table_mapping) + 1
    assert dataframes["public_holidays"].shape == (14, 7)
    assert dataframes["olist_customers"].shape == (99441, 5)
    assert dataframes["olist_geolocation"].shape == (1000163, 5)
    assert dataframes["olist_order_items"].shape == (112650, 7)
    assert dataframes["olist_order_payments"].shape == (103886, 5)
    assert dataframes["olist_order_reviews"].shape == (99224, 7)
    assert dataframes["olist_orders"].shape == (99441, 8)
    assert dataframes["olist_products"].shape == (32951, 9)
    assert dataframes["olist_sellers"].shape == (3095, 4)
    assert dataframes["product_category_name_translation"].shape == (71, 2)
