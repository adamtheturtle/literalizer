import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(true),
    JSONValue("hi"),
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue(null),
]);
}
