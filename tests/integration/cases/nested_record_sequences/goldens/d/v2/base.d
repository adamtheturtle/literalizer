import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["a": JSONValue(1)])]),
    JSONValue([JSONValue(["a": JSONValue(2)])]),
]);
}
