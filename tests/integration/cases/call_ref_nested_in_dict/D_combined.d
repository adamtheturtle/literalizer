import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["key": JSONValue(["$ref": JSONValue("my_var")]), "count": JSONValue(42)])]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(["key": JSONValue(["$ref": JSONValue("my_var")]), "count": JSONValue(42)])]),
]);
}
