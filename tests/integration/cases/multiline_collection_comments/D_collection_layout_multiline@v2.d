import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([
        JSONValue(1),
        JSONValue(2),
        JSONValue(3),
    ]),  // inline a
    "b": JSONValue(2),  // inline b
]);
}
