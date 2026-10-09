class _ThingType { dynamic go() => null; }
class _OuterType { final thing = _ThingType(); }
final outer = _OuterType();
final my_data = null;
void main() {
    outer.thing.go();
}
