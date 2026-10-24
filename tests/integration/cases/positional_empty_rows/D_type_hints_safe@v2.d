import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1), JSONValue("value")]), parseJSON("[]")]),
    JSONValue([parseJSON("[]"), JSONValue([JSONValue(2), JSONValue("other")])]),
]);
}
