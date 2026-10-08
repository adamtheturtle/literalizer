import std.json;
void main() {
auto my_data = JSONValue([
    "url": JSONValue("https://example.org/a/*b*/"),
    "count": JSONValue(2),
]);
}
