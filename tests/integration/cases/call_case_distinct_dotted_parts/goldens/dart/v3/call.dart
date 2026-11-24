class _FooType2 { dynamic bar({dynamic x}) => null; }
class _FooType1 { final Foo = _FooType2(); }
class _AType { final foo = _FooType1(); }
final a = _AType();
final my_data = null;
void main() {
    a.foo.Foo.bar(x: <int>[1]);
}
