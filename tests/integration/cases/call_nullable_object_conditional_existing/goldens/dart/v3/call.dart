dynamic make_widget({dynamic count}) => null;
dynamic consume({dynamic count}) => null;
final my_data = null;
void main() {
    var my_data = make_widget(count: 7);
    consume(count: my_data);
    my_data = make_widget(count: 13) != null ?
    make_widget(count: 13) // inner
    : null; // trailing
    consume(count: my_data);
}
