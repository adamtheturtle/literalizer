import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue(3000000000),
    "c": JSONValue("x"),
]);
my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue(3000000000),
    "c": JSONValue("x"),
]);
}
