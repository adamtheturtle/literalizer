import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["timestamp": JSONValue("2020-01-01T00:00:00+00:00")]),
    parseJSON("{}"),
]);
}
