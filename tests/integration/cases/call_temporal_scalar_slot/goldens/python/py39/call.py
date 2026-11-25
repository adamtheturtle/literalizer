import datetime
def process(*_args: object, **_kwargs: object) -> object: ...
process(value=datetime.time(hour=9, minute=30, second=0))
process(value=datetime.datetime(year=2024, month=1, day=15, hour=0, minute=0, second=0, tzinfo=datetime.UTC))
process(value=1)
