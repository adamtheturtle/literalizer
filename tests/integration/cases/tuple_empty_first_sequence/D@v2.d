import std.json;
void main() {
auto my_data = JSONValue([
    parseJSON("[]"),
    JSONValue([JSONValue(1), JSONValue("value")]),
    JSONValue([JSONValue(2), JSONValue("other")]),
]);
}
