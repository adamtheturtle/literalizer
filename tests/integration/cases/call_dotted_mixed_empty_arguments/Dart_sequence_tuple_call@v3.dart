class _ThingType { dynamic go({dynamic before, dynamic populated, dynamic after}) => null; }
final thing = _ThingType();
final my_data = null;
void main() {
    thing.go(before: (), populated: (1,), after: ());
    thing.go(before: ("text",), populated: (2,), after: ());
    thing.go(before: (), populated: ("text",), after: ());
    thing.go(before: ("text",), populated: (2,), after: (3,));
}
