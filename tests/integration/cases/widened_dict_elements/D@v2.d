import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([parseJSON("{}"), JSONValue(["x": JSONValue(1)])]),
    "b": JSONValue([parseJSON("[]"), JSONValue([JSONValue(1)])]),
]);
}
