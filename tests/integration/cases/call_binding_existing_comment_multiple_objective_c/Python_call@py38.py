def make_widget(*_args: object, **_kwargs: object) -> object: ...
my_data = 42
my_data = make_widget(count=my_data) // note
// extra
make_widget(count=my_data)
