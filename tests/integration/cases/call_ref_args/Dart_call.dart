dynamic process({dynamic data, dynamic count}) => null;
final my_data = null;
void main() {
    final my_var = <int>[
        1,
        2,
        3,
    ];
    final my_other = <int>[
        4,
        5,
        6,
    ];
    process(data: my_var, count: 42);
    process(data: my_other, count: 7);
}
