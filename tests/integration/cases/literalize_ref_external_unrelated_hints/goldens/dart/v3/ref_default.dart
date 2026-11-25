dynamic consume_widget({dynamic arg_value}) => null;
final my_data = null;
void main() {
    final missing = <int>[
        1,
        2,
    ];
    final my_data = missing;
    consume_widget(arg_value: my_data);
}
