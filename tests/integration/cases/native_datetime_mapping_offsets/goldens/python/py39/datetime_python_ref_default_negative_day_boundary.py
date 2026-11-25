import datetime
binding = {
    "stamp": datetime.datetime(year=2001, month=2, day=3, hour=4, minute=5, second=6, microsecond=123456, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=-23, minutes=-59, seconds=-59, microseconds=-999999))),
    datetime.datetime(year=2001, month=2, day=3, hour=4, minute=5, second=6, microsecond=123456, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=-23, minutes=-59, seconds=-59, microseconds=-999999))): "key",
}
result_data = binding
