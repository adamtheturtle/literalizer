dynamic consume({dynamic items, dynamic mapping}) => null;
final my_data = null;
void main() {
    final foo = 42;
    consume(items: <Map<String, int>>[
        <String, dynamic>{
            "other": 1,
        },
        foo,
    ], mapping: <String, int>{
        "left": foo,
        "other": 1,
    });
}
