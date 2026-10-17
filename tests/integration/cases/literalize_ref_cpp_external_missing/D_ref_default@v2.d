import std.json;
void main() {
int consume_widget(T...)(T args) { return 0; }
auto item = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
consume_widget(my_data);
my_data = item;
consume_widget(my_data);
}
