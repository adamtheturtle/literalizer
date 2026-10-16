import std.json;
void main() {
auto my_data = JSONValue([
    "_": JSONValue([JSONValue(["type": JSONValue("create"), "name": JSONValue("a")]), JSONValue(["type": JSONValue("update"), "name": JSONValue("b")])]),
]);
}
