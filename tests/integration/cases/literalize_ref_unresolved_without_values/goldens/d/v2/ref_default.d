import std.json;
void main() {
int consume_widget(T...)(T args) { return 0; }
auto a = JSONValue(0);
auto my_data = JSONValue([
    a,
    JSONValue(1),
]);
consume_widget(my_data);
}
