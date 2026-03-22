import std.json;

void _check() {
auto my_data = JSONValue([
    JSONValue("foo"),
    JSONValue("bar"),
    JSONValue("baz"),
]);
my_data = JSONValue([
    JSONValue("foo"),
    JSONValue("bar"),
    JSONValue("baz"),
]);
}
