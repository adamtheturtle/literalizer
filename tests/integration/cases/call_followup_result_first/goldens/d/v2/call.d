import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
int consume(T...)(T args) { return 0; }
auto my_data = make_widget(42, 3);
consume(my_data, 3);
}
