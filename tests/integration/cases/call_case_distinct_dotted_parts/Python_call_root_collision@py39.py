class _FooType:
    def bar(self, *_args: object, **_kwargs: object) -> object: ...
class _FooType:
    Foo = _FooType()
foo = _FooType()
foo.Foo.bar(x=(1,))
