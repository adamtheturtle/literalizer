import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([parseJSON("[]")]),
    JSONValue([parseJSON("[]")]),
]);
my_data = JSONValue([
    JSONValue([parseJSON("[]")]),
    JSONValue([parseJSON("[]")]),
]);
}
