import std.json;
void main() {
auto my_data = JSONValue([
    "description": JSONValue("# not a comment\n"),
    "name": JSONValue("foo"),
]);
}
