import std.json;
void main() {
auto my_data = JSONValue([
    "outer": JSONValue(["a": JSONValue(1), "b": JSONValue("x"), "c": JSONValue(null)]),
]);
my_data = JSONValue([
    "outer": JSONValue(["a": JSONValue(1), "b": JSONValue("x"), "c": JSONValue(null)]),
]);
}
