def process(*_args: object, **_kwargs: object) -> object: ...
my_var = 42
my_other = 7
process(data=({"ref": "my_var"}, 42, "static"))
process(data=({"ref": "my_other"}, 7, "label"))
