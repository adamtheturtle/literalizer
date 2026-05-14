import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["x": JSONValue(1)]),
    "b": JSONValue(2),
]);
my_data = JSONValue([
    "a": JSONValue(["x": JSONValue(1)]),
    "b": JSONValue(2),
]);
}
