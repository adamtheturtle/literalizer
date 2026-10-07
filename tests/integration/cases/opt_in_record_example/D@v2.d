import std.json;
void main() {
auto my_data = JSONValue([
    "name": JSONValue("Ada"),
    "active": JSONValue(true),
    "scores": JSONValue([JSONValue(1), JSONValue(2), JSONValue(3)]),
]);
}
