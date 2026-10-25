import std.json;
void main() {
int consume_widget(T...)(T args) { return 0; }
auto missing = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
auto my_data = missing;
consume_widget(my_data);
}
