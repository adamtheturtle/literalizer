dynamic make_widget({dynamic count}) => null;
final my_data = null;
void main() {
    final my_data = make_widget(count: null);
    my_data = make_widget(count: 42); // note
    // extra
}
