dynamic raw_value({dynamic value}) => null;
dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    var my_data = raw_value(value: 42);
    consume(value: my_data);
    my_data = raw_value(value: 42); // note
    consume(value: my_data);
}
