import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["timestamp": JSONValue(1577836800)]),
    parseJSON("{}"),
]);
}
