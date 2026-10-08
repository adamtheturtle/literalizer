class _FooType { dynamic class({dynamic value}) => null; }
final foo = _FooType();
final my_data = null;
void main() {
    foo.class(value: 1);
}
