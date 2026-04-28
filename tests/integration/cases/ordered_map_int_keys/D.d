import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("1"), JSONValue("one")]),
    JSONValue([JSONValue("2"), JSONValue("two")]),
    JSONValue([JSONValue("42"), JSONValue("answer")]),
]);
}
