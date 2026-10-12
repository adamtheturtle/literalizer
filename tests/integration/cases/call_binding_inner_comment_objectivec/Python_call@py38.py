def make_widget(*_args: object, **_kwargs: object) -> object: ...
my_data = make_widget(count=42) ?
make_widget(count=42) // inner
: nil // trailing
