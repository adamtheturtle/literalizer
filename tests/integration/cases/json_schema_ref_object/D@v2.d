import std.json;
void main() {
auto my_data = JSONValue([
    "schema": JSONValue(["$ref": JSONValue("#/defs/Foo")]),
]);
}
