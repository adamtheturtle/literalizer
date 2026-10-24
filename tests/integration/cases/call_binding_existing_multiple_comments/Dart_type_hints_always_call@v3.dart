dynamic make_widget({dynamic count}) => null;
dynamic consume_widget({dynamic count}) => null;
final my_data = null;
void main() {
    var my_data = make_widget(count: 42);
    consume_widget(count: my_data);
    my_data = make_widget(count: 42); // note
    // extra
    consume_widget(count: my_data);
}
