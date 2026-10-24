import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue([JSONValue(1)]), JSONValue([JSONValue(2)])]),
    "b": JSONValue([JSONValue([JSONValue("x")]), JSONValue([JSONValue("y")])]),
]);
}
