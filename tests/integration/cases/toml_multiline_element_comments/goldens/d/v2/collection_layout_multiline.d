import std.json;
void main() {
auto my_data = JSONValue([
    "first": JSONValue([
        JSONValue(1),
        JSONValue(2),
    ]),
    "second": JSONValue(3),  // About the second key.
]);
}
