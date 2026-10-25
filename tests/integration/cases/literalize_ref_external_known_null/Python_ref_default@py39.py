def consume_widget(*_args: object, **_kwargs: object) -> object: ...
item = None
my_data = None
consume_widget(arg_value=my_data)
my_data = item
consume_widget(arg_value=my_data)
