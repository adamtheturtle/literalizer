import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("first"), JSONValue("one")]),
    JSONValue([JSONValue("second"), JSONValue("two")]),
    JSONValue([JSONValue("third"), JSONValue("three")]),
]);
}
