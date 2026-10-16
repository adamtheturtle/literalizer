import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue("x"),
    "e": JSONValue([JSONValue(1), JSONValue(2)]),
    "f": JSONValue(["g": JSONValue("h")]),
]);
}
