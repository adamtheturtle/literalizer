import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(["$ref": JSONValue("my_var")]), JSONValue(42), JSONValue("static")])]),
    JSONValue([JSONValue([JSONValue(["$ref": JSONValue("my_other")]), JSONValue(7), JSONValue("label")])]),
]);
}
