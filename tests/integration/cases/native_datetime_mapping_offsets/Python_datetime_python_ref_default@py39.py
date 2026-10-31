import datetime
binding = {
    "stamp": datetime.datetime(year=2001, month=2, day=3, hour=4, minute=5, second=6, microsecond=123456, tzinfo=datetime.UTC),
    datetime.datetime(year=2001, month=2, day=3, hour=4, minute=5, second=6, microsecond=123456, tzinfo=datetime.UTC): "key",
}
result_data = binding
