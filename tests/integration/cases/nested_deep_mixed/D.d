import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1), JSONValue(2)]), JSONValue([JSONValue("a"), JSONValue("b")])]),
]);
}
