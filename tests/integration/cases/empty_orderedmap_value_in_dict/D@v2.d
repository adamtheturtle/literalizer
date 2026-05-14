import std.json;
void main() {
auto my_data = JSONValue([
    "a": parseJSON("{}"),
    "b": JSONValue(1),
]);
}
