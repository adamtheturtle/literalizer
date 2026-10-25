import std.json;
void main() {
auto my_data = JSONValue([
    "left": JSONValue([JSONValue(1), JSONValue("one")]),
    "right": JSONValue([JSONValue(2), JSONValue("two")]),
]);
}
