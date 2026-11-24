import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(2), JSONValue("hello")]),  // trailing note
    // next element
    JSONValue([JSONValue(3), JSONValue("world")]),
]);
}
