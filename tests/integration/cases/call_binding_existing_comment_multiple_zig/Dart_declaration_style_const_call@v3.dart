dynamic make_widget({dynamic count}) => null;
final my_data = null;
void main() {
    const my_data = make_widget(count: 42);
    my_data = make_widget(count: 42); // note
    // extra
}
