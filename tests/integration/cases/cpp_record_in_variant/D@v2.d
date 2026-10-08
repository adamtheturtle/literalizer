import std.json;
void main() {
auto my_data = JSONValue([
    "h": JSONValue([JSONValue(1), JSONValue("a"), JSONValue([JSONValue(2), JSONValue("b")]), JSONValue(["k": JSONValue([JSONValue(true)])])]),
]);
}
