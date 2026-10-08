def f(*_args: object, **_kwargs: object) -> object: ...
ref_data = (
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
        ref_data,
    ),
))
