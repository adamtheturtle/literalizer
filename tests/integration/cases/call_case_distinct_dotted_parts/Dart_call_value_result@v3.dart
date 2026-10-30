class _FooType { dynamic bar({dynamic x}) => null; }
class _FooType { final Foo = _FooType(); }
class _AType { final foo = _FooType(); }
final a = _AType();
final my_data = a.foo.Foo.bar(x: <int>[1]);
