import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    parseJSON("[]"),
    JSONValue([JSONValue("a"), JSONValue("b")]),
]);
my_data = JSONValue([
    JSONValue([JSONValue(1), JSONValue(2)]),
    parseJSON("[]"),
    JSONValue([JSONValue("a"), JSONValue("b")]),
]);
}
