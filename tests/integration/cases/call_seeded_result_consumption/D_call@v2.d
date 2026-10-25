import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
int consume_widget(T...)(T args) { return 0; }
auto my_data = make_widget(0);
consume_widget(my_data);
my_data = make_widget(1);
consume_widget(my_data);
}
