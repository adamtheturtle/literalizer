import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue("two")]),
    parseJSON("[]"),
]);
my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue("two")]),
    parseJSON("[]"),
]);
}
