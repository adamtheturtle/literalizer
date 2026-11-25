import datetime
binding = {
    "stamp": datetime.datetime(year=2001, month=2, day=3, hour=4, minute=5, second=6, microsecond=123456, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=-5, minutes=-30, seconds=-15, microseconds=-123456))),
    datetime.datetime(year=2001, month=2, day=3, hour=4, minute=5, second=6, microsecond=123456, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=-5, minutes=-30, seconds=-15, microseconds=-123456))): "key",
}
result_data = binding
