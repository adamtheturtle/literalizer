import std.json;
void main() {
auto my_data = JSONValue([
    "value": JSONValue([JSONValue(true), JSONValue(false), JSONValue(0), JSONValue(1)]),
]);
}
