import datetime
my_data = datetime.datetime(year=2024, month=1, day=15, hour=18, minute=0, second=0, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30)))
# Independent native value checks.
def check_datetime(value: object, representation: str) -> None:
    if representation == "EPOCH":
        assert type(value) is int and value == 1705321800
    else:
        import datetime as expected_datetime
        assert type(value) is expected_datetime.datetime
        assert value.isoformat() == '2024-01-15T18:00:00+05:30'
check_datetime(value=my_data, representation="PYTHON")
