def process(*_args: object, **_kwargs: object) -> object: ...
my_list = {
    "unused": "value",
}
process(data=(({"inner": my_list},),))
