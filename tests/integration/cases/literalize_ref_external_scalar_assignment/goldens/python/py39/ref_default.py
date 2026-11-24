def consume_widget(*_args: object, **_kwargs: object) -> object: ...
my_data = 0
shared = 1
consume_widget(arg_value=my_data)
my_data = shared
consume_widget(arg_value=my_data)
