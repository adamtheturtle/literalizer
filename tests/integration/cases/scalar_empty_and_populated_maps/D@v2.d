import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(1),
    parseJSON("{}"),
    JSONValue(["x": JSONValue(2)]),
]);
}
