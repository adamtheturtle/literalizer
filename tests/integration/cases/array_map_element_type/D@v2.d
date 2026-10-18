import std.json;
void main() {
auto my_data = JSONValue([
    "d": JSONValue([JSONValue(["a": JSONValue([JSONValue(["b": JSONValue([JSONValue(1), JSONValue([JSONValue(2.5), JSONValue([JSONValue("x"), JSONValue([JSONValue(true)])])])])])])])]),
]);
}
