import datetime
my_data = {
    datetime.date(year=2024, month=1, day=1): "new_year",
    datetime.date(year=2024, month=7, day=4): "independence_day",
    datetime.date(year=2024, month=12, day=25): "christmas",
}
# Independent native value checks.
import datetime as expected_datetime
assert all(type(key) is expected_datetime.date for key in my_data)
assert {key.isoformat(): value for key, value in my_data.items()} == {"2024-01-01": "new_year", "2024-07-04": "independence_day", "2024-12-25": "christmas"}
