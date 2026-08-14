def f(*_args: object, **_kwargs: object) -> object: ...
x = (
    (
        1,
        2,
    ),
    (
        3,
        4,
    ),
)
f(value=(
    (
        x,
    ),
))
