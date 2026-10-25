import std.json;
void main() {
auto my_data = JSONValue([
    "lists": JSONValue([JSONValue([JSONValue(1)]), JSONValue([JSONValue("x")]), parseJSON("[]")]),
    "maps": JSONValue([JSONValue(["x": JSONValue(1)]), JSONValue(["x": JSONValue("s")])]),
    "empties": JSONValue(["a": JSONValue([JSONValue(1)]), "b": parseJSON("[]")]),
]);
}
