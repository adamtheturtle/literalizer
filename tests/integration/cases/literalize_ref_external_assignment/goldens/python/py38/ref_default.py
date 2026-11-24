def consume_widget(*_args: object, **_kwargs: object) -> object: ...
ref_data = (
    1,
    2,
)
my_data = (
    0,
)
consume_widget(arg_value=my_data)
my_data = ref_data
consume_widget(arg_value=my_data)
