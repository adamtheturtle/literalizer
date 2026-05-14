import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(true), JSONValue(false)]),
    JSONValue([JSONValue(true), JSONValue(true)]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(true), JSONValue(false)]),
    JSONValue([JSONValue(true), JSONValue(true)]),
]);
}
