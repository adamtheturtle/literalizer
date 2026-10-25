import std.json;
void main() {
int consume_widget(T...)(T args) { return 0; }
auto item = JSONValue(null);
auto my_data = JSONValue(null);
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
}
