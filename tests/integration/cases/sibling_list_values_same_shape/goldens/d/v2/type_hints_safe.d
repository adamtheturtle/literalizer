import std.json;
void main() {
auto my_data = JSONValue([
    "test": JSONValue([JSONValue(5), JSONValue([JSONValue("compile"), JSONValue("test")])]),
    "package": JSONValue([JSONValue(7), JSONValue([JSONValue("link"), JSONValue("test")])]),
]);
}
