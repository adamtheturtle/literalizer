import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["k": JSONValue("2040-01-01T00:00:00+00:00")]),
    JSONValue(["k": JSONValue(1)]),
]);
}
