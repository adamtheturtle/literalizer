class _ThingType { dynamic go({dynamic before, dynamic populated, dynamic after}) => null; }
final thing = _ThingType();
final my_data = null;
void main() {
    thing.go(before: [], populated: <int>[1], after: []);
    thing.go(before: <String>["text"], populated: <int>[2], after: []);
    thing.go(before: [], populated: <String>["text"], after: []);
    thing.go(before: <String>["text"], populated: <int>[2], after: <int>[3]);
}
