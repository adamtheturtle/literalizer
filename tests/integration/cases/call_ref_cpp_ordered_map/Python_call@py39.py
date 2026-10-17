from collections import OrderedDict
def process(*_args: object, **_kwargs: object) -> object: ...
big_list = (
    "x",
)
process(a=OrderedDict([("m", big_list)]))
