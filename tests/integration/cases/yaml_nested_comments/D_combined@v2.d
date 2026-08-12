import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([
        // inner note
        "b": JSONValue(1),  // inline b
    ]),
    "list": JSONValue([
        JSONValue(1),  // first
        JSONValue(2),  // second
    ]),
]);
my_data = JSONValue([
    "a": JSONValue([
        // inner note
        "b": JSONValue(1),  // inline b
    ]),
    "list": JSONValue([
        JSONValue(1),  // first
        JSONValue(2),  // second
    ]),
]);
}
