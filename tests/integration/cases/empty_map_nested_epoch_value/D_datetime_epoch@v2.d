import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["nested": JSONValue(["times": JSONValue([JSONValue(-2208988800)])])]),
    parseJSON("{}"),
]);
}
