import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0b1),
    JSONValue("hello"),
    JSONValue(true),
    JSONValue(null),
]);
}
