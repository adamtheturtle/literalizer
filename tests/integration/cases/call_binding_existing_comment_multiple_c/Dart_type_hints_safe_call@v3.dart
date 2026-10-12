dynamic make_widget({dynamic count}) => null;
final my_data = null;
void main() {
    final my_data = 42;
    my_data = make_widget(count: my_data); // note
    // extra
    make_widget(count: my_data);
}
