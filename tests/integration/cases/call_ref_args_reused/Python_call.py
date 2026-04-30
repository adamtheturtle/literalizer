def process(*_args: object, **_kwargs: object) -> object: ...
shared = 1
other = 2
process(data=shared, count=1)
process(data=other, count=0)
process(data=shared, count=8)
