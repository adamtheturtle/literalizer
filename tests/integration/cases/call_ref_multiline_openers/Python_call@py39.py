def consume(*_args: object, **_kwargs: object) -> object: ...
foo = 42
consume(items=(
    {
        "other": 1,
    },
    foo,
), mapping={
    "left": foo,
    "other": 1,
})
