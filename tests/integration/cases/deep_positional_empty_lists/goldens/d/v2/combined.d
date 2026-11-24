import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([parseJSON("[]")])]),
    JSONValue([JSONValue([JSONValue([JSONValue(1)])])]),
]);
my_data = JSONValue([
    JSONValue([JSONValue([parseJSON("[]")])]),
    JSONValue([JSONValue([JSONValue([JSONValue(1)])])]),
]);
}
