import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["nested": JSONValue(["count": JSONValue(1), "name": JSONValue("value")])]),
    parseJSON("{}"),
]);
}
