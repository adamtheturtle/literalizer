import std.json;
void main() {
auto my_data = JSONValue([
    parseJSON("[]"),
    JSONValue([JSONValue(1)]),
    JSONValue([JSONValue(1), JSONValue(2)]),
    JSONValue([JSONValue(1), JSONValue("x"), JSONValue(true), JSONValue(null)]),
    JSONValue([JSONValue(1), JSONValue(2), JSONValue(3), JSONValue(4), JSONValue(5), JSONValue(6), JSONValue(7), JSONValue(8)]),
]);
}
