import std.json;
void main() {
auto my_data = JSONValue([
    "lint": JSONValue([JSONValue(2), JSONValue([JSONValue(1)])]),
    "test": JSONValue([JSONValue(5), JSONValue([JSONValue(7)])]),
]);
my_data = JSONValue([
    "lint": JSONValue([JSONValue(2), JSONValue([JSONValue(1)])]),
    "test": JSONValue([JSONValue(5), JSONValue([JSONValue(7)])]),
]);
}
