import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["$ref": JSONValue("repeated_var")]), JSONValue(1)]),
    JSONValue([JSONValue(["$ref": JSONValue("single_var")]), JSONValue(0)]),
    JSONValue([JSONValue(["$ref": JSONValue("repeated_var")]), JSONValue(8)]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(["$ref": JSONValue("repeated_var")]), JSONValue(1)]),
    JSONValue([JSONValue(["$ref": JSONValue("single_var")]), JSONValue(0)]),
    JSONValue([JSONValue(["$ref": JSONValue("repeated_var")]), JSONValue(8)]),
]);
}
