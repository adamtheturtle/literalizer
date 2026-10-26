import std.json;
void main() {
auto my_data = JSONValue([
    "numbers": JSONValue([JSONValue(1), JSONValue(2)]),
    "nested": JSONValue(["inner": JSONValue([JSONValue(3)])]),
    "mixed": JSONValue([JSONValue(4), JSONValue("five")]),
]);
}
