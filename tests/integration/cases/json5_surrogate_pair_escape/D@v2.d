import std.json;
void main() {
auto my_data = JSONValue([
    "astral": JSONValue("😀"),
    "mixed": JSONValue("a😀b"),
    "count": JSONValue(2),
    "list": JSONValue([JSONValue("😀"), JSONValue(1)]),
    "nested": JSONValue(["inner": JSONValue("😀")]),
]);
}
