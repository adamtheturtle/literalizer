import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([JSONValue(1)]),
    "b": parseJSON("[]"),
]);
}
