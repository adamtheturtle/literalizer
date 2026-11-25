import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["k": JSONValue("2020-01-01T00:00:00+00:00")]),
    "b": JSONValue(["k": JSONValue("string")]),
]);
}
