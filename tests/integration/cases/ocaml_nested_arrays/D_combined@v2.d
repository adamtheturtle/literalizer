import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1)])]),
    JSONValue([parseJSON("[]")]),
]);
my_data = JSONValue([
    JSONValue([JSONValue([JSONValue(1)])]),
    JSONValue([parseJSON("[]")]),
]);
}
