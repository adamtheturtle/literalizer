import std.json;
void main() {
auto my_data = JSONValue([
    "first": JSONValue([JSONValue([JSONValue(1), JSONValue("value")]), parseJSON("[]")]),
    "second": JSONValue([parseJSON("[]"), JSONValue([JSONValue(2), JSONValue("other")])]),
]);
}
