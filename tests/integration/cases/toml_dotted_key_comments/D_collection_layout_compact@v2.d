import std.json;
void main() {
auto my_data = JSONValue([
    // first dotted key
    // second dotted key
    "a": JSONValue(["b": JSONValue(1), "c": JSONValue(2)]),
]);
}
