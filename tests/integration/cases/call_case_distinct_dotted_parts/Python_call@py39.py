class _FooType:
    def bar(self, *_args: object, **_kwargs: object) -> object: ...
class _FooType:
    Foo = _FooType()
class _AType:
    foo = _FooType()
a = _AType()
a.foo.Foo.bar(x=(1,))
