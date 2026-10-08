import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([parseJSON("[]"), parseJSON("[]")]),
    JSONValue([JSONValue([JSONValue(1)]), JSONValue([JSONValue(1)])]),
]);
my_data = JSONValue([
    JSONValue([parseJSON("[]"), parseJSON("[]")]),
    JSONValue([JSONValue([JSONValue(1)]), JSONValue([JSONValue(1)])]),
]);
}
