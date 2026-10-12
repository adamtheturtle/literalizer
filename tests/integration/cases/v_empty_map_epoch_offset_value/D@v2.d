import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["timestamp": JSONValue("2040-01-01T03:00:00+03:00")]),
    parseJSON("{}"),
]);
}
