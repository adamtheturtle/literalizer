import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue([parseJSON("[]"), parseJSON("[]")]),
]);
my_data = JSONValue([
    JSONValue([parseJSON("[]"), parseJSON("[]")]),
]);
}
