dynamic process({dynamic data, dynamic count}) => null;
final my_data = null;
void main() {
    final single_var = <int>[
        4,
        5,
        6,
    ];
    final repeated_var = 1;
    process(data: repeated_var, count: 1);
    process(data: single_var, count: 0);
    process(data: repeated_var, count: 8);
}
