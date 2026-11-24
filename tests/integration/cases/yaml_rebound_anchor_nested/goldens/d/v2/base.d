import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(1), JSONValue([JSONValue(2)]), JSONValue(2)]),
]);
}
