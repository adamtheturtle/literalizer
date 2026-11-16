dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final item = 42;
    consume(value: <String, int>{"field": item});
}
