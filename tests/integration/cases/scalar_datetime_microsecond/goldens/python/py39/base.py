import datetime
my_data = datetime.datetime(year=2024, month=1, day=15, hour=12, minute=30, second=0, microsecond=123456, tzinfo=datetime.UTC)
# Independent native value checks.
import datetime as expected_datetime
assert type(my_data) is expected_datetime.datetime
assert my_data.isoformat() == '2024-01-15T12:30:00.123456+00:00'
