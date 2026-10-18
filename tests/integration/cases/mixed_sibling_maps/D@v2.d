import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["a": JSONValue(1)]), JSONValue(["a": JSONValue(null)]), JSONValue(42)]),
    JSONValue([JSONValue(["a": JSONValue(1)]), JSONValue(["a": JSONValue("s")]), JSONValue(42)]),
    JSONValue([JSONValue(["a": JSONValue(1)]), JSONValue(["a": JSONValue(null)])]),
    JSONValue([JSONValue(["a": JSONValue(1)]), JSONValue(["a": JSONValue("s")])]),
]);
}
