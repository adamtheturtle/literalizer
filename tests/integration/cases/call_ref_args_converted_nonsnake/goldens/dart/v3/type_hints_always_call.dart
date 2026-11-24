dynamic process({dynamic data, dynamic count}) => null;
final my_data = null;
void main() {
    final List<int> myVar = <int>[
        1,
        2,
        3,
    ];
    final List<int> myOther = <int>[
        4,
        5,
        6,
    ];
    process(data: myVar, count: 42);
    process(data: myOther, count: 7);
}
