def consume_widget(*_args: object, **_kwargs: object) -> object: ...
item = (
    1,
    2,
)
my_data = (
    1,
    2,
)
consume_widget(arg_value=my_data)
my_data = item
consume_widget(arg_value=my_data)
