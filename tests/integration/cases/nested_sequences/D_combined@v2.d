import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1), JSONValue(2)]), JSONValue([JSONValue(3), JSONValue(4)])]),
    JSONValue([JSONValue([JSONValue(5)])]),
]);
my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1), JSONValue(2)]), JSONValue([JSONValue(3), JSONValue(4)])]),
    JSONValue([JSONValue([JSONValue(5)])]),
]);
}
