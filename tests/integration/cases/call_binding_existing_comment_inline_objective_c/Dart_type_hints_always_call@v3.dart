dynamic make_widget({dynamic count}) => null;
final my_data = null;
void main() {
    final int my_data = 42;
    my_data = make_widget(count: my_data); // note
    make_widget(count: my_data);
}
