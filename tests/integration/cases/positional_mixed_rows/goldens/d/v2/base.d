import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1), JSONValue("value")]), JSONValue([JSONValue(1), JSONValue(2)]), parseJSON("[]")]),
    JSONValue([parseJSON("[]"), parseJSON("[]"), JSONValue([JSONValue(3), JSONValue(4)])]),
]);
}
