class _FooBarType2:
    def bar(self, *_args: object, **_kwargs: object) -> object: ...
class _FooBarType1:
    fooBar = _FooBarType2()
class _AType:
    foo_bar = _FooBarType1()
a = _AType()
a.foo_bar.fooBar.bar(x=(1,))
