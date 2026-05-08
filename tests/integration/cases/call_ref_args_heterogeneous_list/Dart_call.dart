dynamic process({dynamic data, dynamic count}) => null;
final my_data = null;
void main() {
    final my_ints = <int>[
        1,
        2,
        3,
    ];
    final my_strings = <String>[
        "a",
        "b",
    ];
    final my_empty = [];
    process(data: my_ints, count: 42);
    process(data: my_strings, count: 7);
    process(data: my_empty, count: 99);
}
