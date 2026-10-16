dynamic make_widget({dynamic count}) => null;
final my_data = null;
void main() {
    final my_data = make_widget(count: 42);
    make_widget(count: my_data);
    my_data = make_widget(count: my_data);
    // note
    make_widget(count: my_data);
}
