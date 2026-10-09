import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["mapping": parseJSON("{}")]),
    parseJSON("{}"),
]);
}
