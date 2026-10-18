def consume_widget(*_args: object, **_kwargs: object) -> object: ...
shared = (
    1,
    2,
)
my_data = shared
consume_widget(arg_value=my_data)
