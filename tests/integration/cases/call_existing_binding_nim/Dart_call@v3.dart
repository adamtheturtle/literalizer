dynamic make_widget({dynamic count}) => null;
final my_data = null;
void main() {
    final my_data = make_widget(count: 0);
    my_data = make_widget(count: 1);
    make_widget(count: my_data);
}
