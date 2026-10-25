void main() {
int consume_widget(T...)(T args) { return 0; }
auto my_data = [
    "a": 0,
];
consume_widget(my_data);
my_data = [
    "a": 1,
];
consume_widget(my_data);
}
