import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(["$ref": JSONValue("myVar")]), JSONValue(42), JSONValue("static")])]),
]);
my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(["$ref": JSONValue("myVar")]), JSONValue(42), JSONValue("static")])]),
]);
}
