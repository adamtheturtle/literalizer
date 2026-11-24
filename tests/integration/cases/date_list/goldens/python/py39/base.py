import datetime
my_data = (
    datetime.date(year=2024, month=1, day=15),
    datetime.date(year=2024, month=2, day=20),
)
# Independent native value checks.
import datetime as expected_datetime
assert isinstance(my_data, (list, tuple))
assert all(type(value) is expected_datetime.date for value in my_data)
assert tuple(value.isoformat() for value in my_data) == ("2024-01-15", "2024-02-20")
