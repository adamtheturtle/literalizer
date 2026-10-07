import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue([JSONValue(["b": JSONValue(1)])])]),
]);
my_data = JSONValue([
    "a": JSONValue([JSONValue([JSONValue(["b": JSONValue(1)])])]),
]);
}
