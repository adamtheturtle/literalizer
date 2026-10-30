class _FooType { dynamic bar({dynamic x}) => null; }
class _FooType { final Foo = _FooType(); }
final foo = _FooType();
final my_data = null;
void main() {
    foo.Foo.bar(x: <int>[1]);
}
