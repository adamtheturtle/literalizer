import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["timestamp": JSONValue(2208988800)]),
    parseJSON("{}"),
]);
}
