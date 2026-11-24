class _OuterType { dynamic inner({dynamic outer, dynamic n}) => null; }
final outer = _OuterType();
final my_data = null;
void main() {
    outer.inner(outer: 1, n: 2);
}
