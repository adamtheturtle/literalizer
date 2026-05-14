dynamic process({dynamic value, dynamic count}) => null;
final my_data = null;
void main() {
    final my_int = 1;
    final my_bool = true;
    final my_float = 3.14;
    final my_list = <int>[
        1,
        2,
        3,
    ];
    process(value: my_int, count: 42);
    process(value: my_bool, count: 7);
    process(value: my_float, count: 9);
    process(value: my_list, count: 1);
}
