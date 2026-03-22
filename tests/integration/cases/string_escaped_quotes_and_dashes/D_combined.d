import std.json;
void _check() {
auto my_data = JSONValue("hello \"world\" -- not a comment");
my_data = JSONValue("hello \"world\" -- not a comment");
}
