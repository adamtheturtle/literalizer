import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(null)]),
    parseJSON("[]"),
]);
my_data = JSONValue([
    JSONValue([JSONValue(null)]),
    parseJSON("[]"),
]);
}
