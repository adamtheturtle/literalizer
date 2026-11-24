import std.json;
void main() {
auto my_data = JSONValue([
    "b": JSONValue(["k": JSONValue(1)]),
    "a": JSONValue(["k": JSONValue("2040-01-01T00:00:00+00:00")]),
]);
}
