dynamic make_widget({dynamic value}) => null;
dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    final my_data = make_widget(value: r"a\ // payload"); // note
    consume(value: my_data);
}
