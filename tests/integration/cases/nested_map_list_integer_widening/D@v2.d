import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(1)]),
    "b": JSONValue([JSONValue(1099511627776)]),
]);
}
