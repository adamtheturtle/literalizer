import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue("x")]),
    "b": JSONValue([JSONValue("y")]),
]);
}
