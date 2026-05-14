import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    parseJSON("[]"),
    JSONValue([JSONValue(3), JSONValue(4)]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    parseJSON("[]"),
    JSONValue([JSONValue(3), JSONValue(4)]),
]);
}
