dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final my_null = null;
    final regular_null = null;
    consume(value: my_null);
    consume(value: regular_null);
}
