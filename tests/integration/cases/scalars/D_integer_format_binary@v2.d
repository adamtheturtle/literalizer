import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0b101010),
    JSONValue(3.14),
    JSONValue(true),
    JSONValue(false),
    JSONValue("hello \"world\""),
]);
}
