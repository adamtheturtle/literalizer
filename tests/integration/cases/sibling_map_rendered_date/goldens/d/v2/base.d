import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["k": JSONValue("2020-01-01")]),
    "b": JSONValue(["k": JSONValue("string")]),
]);
}
