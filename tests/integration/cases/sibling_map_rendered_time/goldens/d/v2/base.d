import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(["k": JSONValue("07:30:00")]),
    "b": JSONValue(["k": JSONValue("string")]),
]);
}
