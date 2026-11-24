dynamic make_widget({dynamic value}) => null;
dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    var my_data = make_widget(value: 42);
    consume(value: my_data);
    my_data = make_widget(value: 42);
    consume(value: my_data);
}
