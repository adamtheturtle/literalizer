import std.json;
void main() {
auto my_data = JSONValue([
    "value": JSONValue(["$ref": JSONValue("foo")]),
]);
}
