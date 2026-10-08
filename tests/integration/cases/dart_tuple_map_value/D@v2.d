import std.json;
void main() {
auto my_data = JSONValue([
    "rows": JSONValue([JSONValue(["x": JSONValue(1), "y": JSONValue("a")]), JSONValue(["x": JSONValue(2), "y": JSONValue("b")])]),
]);
}
