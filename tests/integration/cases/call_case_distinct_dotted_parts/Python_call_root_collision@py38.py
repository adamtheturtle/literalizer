class _FooType1:
    def bar(self, *_args: object, **_kwargs: object) -> object: ...
class _FooType0:
    Foo = _FooType1()
foo = _FooType0()
foo.Foo.bar(x=(1,))
