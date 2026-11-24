dynamic raw_value({dynamic value}) => null;
dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final my_data = raw_value(value: 42); // note
    consume(value: my_data);
}
