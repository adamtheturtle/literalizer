def process(data: 'tuple[tuple[dict[object, object], ...], ...]') -> object: ...
my_list = {
    "unused": "value",
}
process(data=(({"inner": my_list},),))
