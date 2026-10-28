def consume(value: 'tuple[object, ...]') -> object: ...
item = (
    1,
    2,
)
consume(value=item)
