import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["b": JSONValue(["c": JSONValue(["$ref": JSONValue("deep")])])]),
]);
my_data = JSONValue([
    "a": JSONValue(["b": JSONValue(["c": JSONValue(["$ref": JSONValue("deep")])])]),
]);
}
