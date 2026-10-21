import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
int consume_widget(T...)(T args) { return 0; }
auto my_data = make_widget(42);
consume_widget(my_data);
my_data = make_widget(42);
// note
consume_widget(my_data);
}
