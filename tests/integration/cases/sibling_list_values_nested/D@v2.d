import std.json;
void main() {
auto my_data = JSONValue([
    "lint": JSONValue([JSONValue(2), parseJSON("[]")]),
    "test": JSONValue([JSONValue(5), JSONValue([JSONValue("compile")])]),
]);
}
