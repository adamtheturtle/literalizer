dynamic make_widget({dynamic count}) => null;
dynamic consume({dynamic count}) => null;
final my_data = null;
void main() {
    var my_data = make_widget(count: null);
    consume(count: my_data);
    my_data = make_widget(count: 42);
    consume(count: my_data);
}
