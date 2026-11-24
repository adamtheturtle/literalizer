import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["k": JSONValue(1)]),
    "b": JSONValue(["k": JSONValue("s")]),
]);
}
