class _FooType2:
    def bar(self, *_args: object, **_kwargs: object) -> object: ...
class _FooType1:
    Foo = _FooType2()
class _AType:
    foo = _FooType1()
a = _AType()
a.foo.Foo.bar(x=(1,))
