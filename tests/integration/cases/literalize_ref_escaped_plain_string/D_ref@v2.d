import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0),
    JSONValue([JSONValue([JSONValue("plain")])]),
]);
}
