from collections import OrderedDict
my_data: tuple[str | OrderedDict[str, int], ...] = (
    OrderedDict([("a", 1)]),
    "hello",
)
