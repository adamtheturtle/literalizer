import std.json;
void main() {
auto actual = JSONValue(42);
auto my_data = JSONValue([
    JSONValue(["$ref": JSONValue(1)]),
    JSONValue(["$ref": JSONValue(null)]),
    actual,
]);
}
