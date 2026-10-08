import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["a": JSONValue([JSONValue(1)])]),
    JSONValue(["a": JSONValue([JSONValue(2)])]),
]);
}
