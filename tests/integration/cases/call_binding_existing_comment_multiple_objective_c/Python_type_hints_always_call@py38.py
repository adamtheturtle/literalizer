def make_widget(*_args: object, **_kwargs: object) -> object: ...
my_data = make_widget(count=42)
make_widget(count=my_data)
my_data = make_widget(count=my_data) // note
// extra
make_widget(count=my_data)
