import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["a": JSONValue(1)]),
    JSONValue(1),
    JSONValue("x"),
    JSONValue(true),
    JSONValue(2.5),
    JSONValue(null),
]);
}
