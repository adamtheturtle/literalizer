import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("]"),
    JSONValue("a]"),
    JSONValue("a]="),
    JSONValue("a]b"),
]);
}
