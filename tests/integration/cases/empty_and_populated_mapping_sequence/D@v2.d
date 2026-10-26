import std.json;
void main() {
auto my_data = JSONValue([
    parseJSON("{}"),
    JSONValue(["value": JSONValue(1)]),
]);
}
