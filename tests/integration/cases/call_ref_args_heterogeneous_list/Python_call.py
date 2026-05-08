def process(*_args: object, **_kwargs: object) -> object: ...
my_ints = (
    1,
    2,
    3,
)
my_strings = (
    "a",
    "b",
)
process(data=my_ints, count=42)
process(data=my_strings, count=7)
