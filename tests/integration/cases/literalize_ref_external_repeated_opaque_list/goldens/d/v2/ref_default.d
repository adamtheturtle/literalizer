import std.json;
void main() {
int consume_widget(T...)(T args) { return 0; }
auto item = parseJSON("[]");
auto my_data = JSONValue([
    item,
    item,
]);
consume_widget(my_data);
}
