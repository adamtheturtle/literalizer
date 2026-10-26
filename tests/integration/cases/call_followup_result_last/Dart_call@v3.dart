dynamic make_widget({dynamic first, dynamic second}) => null;
dynamic consume({dynamic first, dynamic second}) => null;
final my_data = null;
void main() {
    final my_data = make_widget(first: 42, second: 3);
    consume(first: 3, second: my_data);
}
