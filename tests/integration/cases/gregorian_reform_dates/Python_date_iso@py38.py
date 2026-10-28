import datetime
my_data = {
    "before_date": "1582-10-04",
    "gap_date": "1582-10-10",
    "transition_date": "1582-10-15",
    "after_date": "1582-10-16",
    "before_naive": datetime.datetime(year=1582, month=10, day=4, hour=12, minute=30, second=0, microsecond=1),
    "gap_naive": datetime.datetime(year=1582, month=10, day=10, hour=12, minute=30, second=0, microsecond=500000),
    "transition_positive": datetime.datetime(year=1582, month=10, day=15, hour=0, minute=30, second=0, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=18))),
    "transition_negative": datetime.datetime(year=1582, month=10, day=15, hour=23, minute=30, second=0, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=-18))),
    "after_positive": datetime.datetime(year=1582, month=10, day=16, hour=0, minute=30, second=0, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=18))),
}
