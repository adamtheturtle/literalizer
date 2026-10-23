import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["items": JSONValue([JSONValue(["inner": JSONValue(["x": JSONValue(1)])]), JSONValue(["inner": parseJSON("{}")])])]),
    JSONValue(["items": JSONValue([JSONValue(["inner": JSONValue(["x": JSONValue(2)])]), JSONValue(["inner": parseJSON("{}")])])]),
]);
}
