dynamic consume_widget({dynamic arg_value}) => null;
final my_data = null;
void main() {
    final shared = <int>[
        1,
        2,
    ];
    final my_data = shared;
    consume_widget(arg_value: my_data);
}
