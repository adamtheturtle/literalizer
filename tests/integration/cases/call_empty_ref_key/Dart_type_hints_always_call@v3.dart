dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final int external_value = 1;
    consume(value: external_value);
}
