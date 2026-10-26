dynamic make_widget({dynamic first, dynamic second}) => null;
dynamic consume({dynamic first, dynamic second}) => null;
final my_data = null;
void main() {
    final my_data = make_widget(first: 42, second: 3);
    consume(first: my_data, second: 3);
}
