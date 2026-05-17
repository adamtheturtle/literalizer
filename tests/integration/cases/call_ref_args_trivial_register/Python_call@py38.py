def process(*_args: object, **_kwargs: object) -> object: ...
my_int = 1
my_bool = True
my_float = 3.14
my_list = (
    1,
    2,
    3,
)
process(value=my_int, count=42)
process(value=my_bool, count=7)
process(value=my_float, count=9)
process(value=my_list, count=1)
