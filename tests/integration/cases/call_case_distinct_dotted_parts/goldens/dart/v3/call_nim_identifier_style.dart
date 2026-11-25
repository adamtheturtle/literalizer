class _FoobarType { dynamic bar({dynamic x}) => null; }
class _Foo_BarType { final fooBar = _FoobarType(); }
class _AType { final foo_bar = _Foo_BarType(); }
final a = _AType();
final my_data = null;
void main() {
    a.foo_bar.fooBar.bar(x: <int>[1]);
}
