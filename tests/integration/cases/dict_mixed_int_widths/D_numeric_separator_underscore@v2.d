import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(1),
    "b": JSONValue(3_000_000_000),
    "c": JSONValue("x"),
]);
}
