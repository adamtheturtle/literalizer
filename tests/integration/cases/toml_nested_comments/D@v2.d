import std.json;
void main() {
auto my_data = JSONValue([
    // About the first dotted key.
    // About the second dotted key.
    "dotted": JSONValue(["first": JSONValue(1), "second": JSONValue(2)]),
    "plain": JSONValue(3),  // About the plain key.
    // Inside the table.
    "table": JSONValue(["inner": JSONValue(4)]),
    // Before the first entry.
    // Before the second entry.
    "entries": JSONValue([JSONValue(["name": JSONValue("one")]), JSONValue(["name": JSONValue("two")])]),
]);
}
