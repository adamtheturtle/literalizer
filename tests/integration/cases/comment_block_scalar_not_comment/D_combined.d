import std.json;
void _check() {
auto my_data = JSONValue([
    "description": JSONValue("# not a comment\n"),
    "name": JSONValue("foo"),
]);
my_data = JSONValue([
    "description": JSONValue("# not a comment\n"),
    "name": JSONValue("foo"),
]);
}
