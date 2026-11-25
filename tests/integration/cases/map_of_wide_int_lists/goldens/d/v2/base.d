import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(4294967296), JSONValue(4294967297)]),
]);
}
