import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["count": JSONValue(1), "name": JSONValue("value")]),
    parseJSON("{}"),
]);
}
