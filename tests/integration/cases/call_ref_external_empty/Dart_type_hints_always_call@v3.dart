dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final List<int> item = <int>[
        1,
        2,
    ];
    consume(value: item);
}
