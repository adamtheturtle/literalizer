dynamic f({dynamic value}) => null;
final my_data = null;
void main() {
    final ref_data = <int>[
        1,
        2,
    ];
    f(value: <List<int>>[
        ref_data,
    ]);
    f(value: <List<int>>[
        ref_data,
    ]);
}
