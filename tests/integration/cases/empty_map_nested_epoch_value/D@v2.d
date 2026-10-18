import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["nested": JSONValue(["times": JSONValue([JSONValue("1900-01-01T00:00:00+00:00")])])]),
    parseJSON("{}"),
]);
}
