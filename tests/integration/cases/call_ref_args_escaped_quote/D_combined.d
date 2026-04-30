import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(["$ref": JSONValue("my_str")])]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(["$ref": JSONValue("my_str")])]),
]);
}
