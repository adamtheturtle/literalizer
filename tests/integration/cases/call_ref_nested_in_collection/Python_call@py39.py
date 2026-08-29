def process(*_args: object, **_kwargs: object) -> object: ...
big_list = (
    "x",
)
process(a={"k": big_list}, b=OrderedDict([("m", big_list)]))
