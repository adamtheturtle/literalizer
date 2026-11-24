import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue([
        "b": JSONValue([JSONValue(1)]),
        // Outdented from the sequence, so the inner mapping claims this.
        "c": JSONValue(2),
    ]),
    // Outdented from the inner mapping too, so the root claims this.
    "d": JSONValue(3),
]);
}
