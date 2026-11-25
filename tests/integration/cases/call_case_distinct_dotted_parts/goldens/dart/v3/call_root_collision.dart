class _FooType1 { dynamic bar({dynamic x}) => null; }
class _FooType0 { final Foo = _FooType1(); }
final foo = _FooType0();
final my_data = null;
void main() {
    foo.Foo.bar(x: <int>[1]);
}
