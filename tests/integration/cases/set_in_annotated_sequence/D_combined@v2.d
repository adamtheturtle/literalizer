import std.json;
void main() {
auto my_data = JSONValue([
    parseJSON("[]"),
    JSONValue([JSONValue(1), JSONValue(2)]),
    parseJSON("[]"),
]);
my_data = JSONValue([
    parseJSON("[]"),
    JSONValue([JSONValue(1), JSONValue(2)]),
    parseJSON("[]"),
]);
}
