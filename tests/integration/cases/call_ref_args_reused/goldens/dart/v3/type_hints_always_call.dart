dynamic process({dynamic data, dynamic count}) => null;
final my_data = null;
void main() {
    final List<int> single_var = <int>[
        4,
        5,
        6,
    ];
    final int repeated_var = 1;
    process(data: repeated_var, count: 1);
    process(data: single_var, count: 0);
    process(data: repeated_var, count: 8);
}
