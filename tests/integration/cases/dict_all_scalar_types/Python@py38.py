import datetime
my_data = {
    "s": "string",
    "i": 1,
    "f": 1.5,
    "b": True,
    "n": None,
    "d": datetime.date(year=2024, month=1, day=15),
    "dt": datetime.datetime(year=2024, month=1, day=15, hour=12, minute=0, second=0),
    "by": "48656c6c6f",
}
# Independent native value checks.
import datetime as expected_datetime
assert set(my_data) == {"s", "i", "f", "b", "n", "d", "dt", "by"}
assert my_data["s"] == "string"
assert type(my_data["i"]) is int and my_data["i"] == 1
assert type(my_data["f"]) is float and my_data["f"] == 1.5
assert my_data["b"] is True and my_data["n"] is None
assert type(my_data["d"]) is expected_datetime.date and my_data["d"].isoformat() == "2024-01-15"
assert type(my_data["dt"]) is expected_datetime.datetime and my_data["dt"].isoformat() == "2024-01-15T12:00:00"
assert type(my_data["by"]) is str and my_data["by"] == "48656c6c6f"
