import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(["k": JSONValue(1)])]),
    "b": JSONValue([JSONValue(["k": JSONValue(2)])]),
]);
}
