import std.json;
void main() {
int make_widget(T...)(T args) { return 0; }
auto my_data = make_widget(JSONValue([JSONValue([JSONValue(1), JSONValue(2)]), JSONValue([JSONValue(3)])]));
}
