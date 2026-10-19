import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue([JSONValue(2)])]),
    JSONValue([JSONValue(3), JSONValue([JSONValue(4)])]),
]);
}
